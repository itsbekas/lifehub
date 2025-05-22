import csv
import datetime as dt
import time
from io import StringIO

import requests
from sqlalchemy.orm import Session

from lifehub.core.common.base.api_client import APIException
from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User
from lifehub.providers.trading212.api_client import Trading212APIClient

from ..models import BankBalanceResponse, T212ExportTransaction
from ..repository import AccountBalanceRepository, BankTransactionRepository
from ..schema import AccountBalance, BankAccount, BankTransaction


class Trading212ServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Trading212", status_code, message)


class Trading212Service(BaseUserService):
    _encryption_service: EncryptionService | None = None
    _t212_api: Trading212APIClient | None = None

    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    @property
    def encryption_service(self) -> EncryptionService:
        if self._encryption_service is None:
            self._encryption_service = EncryptionService(self.session, self.user)
        return self._encryption_service

    @property
    def t212_api(self) -> Trading212APIClient:
        if self._t212_api is None:
            self._t212_api = Trading212APIClient(self.user, self.session)
        return self._t212_api

    def fetch_balance(self, account: BankAccount) -> BankBalanceResponse:
        """
        Fetches the latest balance from Trading212 and stores it in the database.
        If the local balance is less than an hour old, it will be returned instead.
        """
        t212_api = Trading212APIClient(self.user, self.session)
        balance_repo = AccountBalanceRepository(self.user, self.session)

        db_balance = balance_repo.get_by_account_id(account.id)

        if db_balance is not None and not account.synced_before(hours=1):
            # Local balance is updated
            balance = db_balance
            balance_amount = float(self.encryption_service.decrypt_data(balance.amount))
        else:
            api_balance = t212_api.get_account_cash()
            if api_balance is None:
                raise Trading212ServiceException(500, "Balance not found")

            balance_amount = float(api_balance.free)
            encrypted_balance = self.encryption_service.encrypt_data(
                str(api_balance.free)
            )

            if db_balance is None:
                balance = AccountBalance(
                    user_id=self.user.id,
                    account_id=account.id,
                    amount=encrypted_balance,
                )
                balance_repo.add(balance)
            else:
                db_balance.amount = encrypted_balance
                balance = db_balance

        res = BankBalanceResponse(
            bank="trading212",
            account_id=str(account.id),
            balance=balance_amount,
        )
        self.session.commit()
        return res

    def _parse_transactions(
        self, account: BankAccount, t212_transactions: list[T212ExportTransaction]
    ) -> list[BankTransaction]:
        transactions = []

        for t in t212_transactions:
            new_t = BankTransaction(
                user_id=self.user.id,
                transaction_id=t.id,
                account_id=account.id,
                date=dt.datetime.fromisoformat(t.time),
            )

            description = None
            counterparty = None
            amount = t.total  # Set separately to handle deposits

            match t.action:
                case "Deposit":
                    description = f"{t.action} ({t.notes})"
                case "Card debit":
                    description = (
                        f"{t.merchant_name} ({t.notes})" if t.notes else t.merchant_name
                    )
                    counterparty = t.merchant_name
                case "Card credit":
                    description = (
                        f"{t.merchant_name} ({t.notes})" if t.notes else t.merchant_name
                    )
                    counterparty = t.merchant_name
                case "Spending cashback":
                    description = t.action
                case "Interest on cash":
                    description = t.action
                case "Lending interest":
                    description = t.notes
                case "Market buy":
                    amount = -amount
                    description = f"{t.action} ({t.ticker})"
                    counterparty = f"{t.name} ({t.ticker})"
                case "Market sell":
                    description = f"{t.action} ({t.ticker})"
                    counterparty = f"{t.name} ({t.ticker})"
                case "Dividend (Dividend)":
                    description = t.action
                    counterparty = f"{t.name} ({t.ticker})"
                case _:
                    pass

            if description is not None:
                new_t.description = self.encryption_service.encrypt_data(description)
            if counterparty is not None:
                new_t.counterparty = self.encryption_service.encrypt_data(counterparty)
            new_t.amount = self.encryption_service.encrypt_data(str(amount))

            transactions.append(new_t)

        return transactions

    def _get_exported_transactions(
        self, to_date: dt.datetime, from_date: dt.datetime
    ) -> list[T212ExportTransaction]:
        export_res = self.t212_api.export_csv(
            include_dividends=True,
            include_interest=True,
            include_orders=True,
            include_transactions=True,
            from_date=from_date,
            to_date=to_date,
        )

        report_id = export_res.reportId

        try:
            time.sleep(3)  # Wait for the export to be generated
            exports_res = self.t212_api.get_exports()
        except APIException as e:
            if e.status_code == 429:
                time.sleep(60)
                exports_res = self.t212_api.get_exports()
            else:
                raise e

        # Get the report with reportId = report_id
        dl_link = next(
            (r.downloadLink for r in exports_res if r.reportId == report_id), None
        )

        if not dl_link:
            # Try up to 5 times
            for _ in range(5):
                time.sleep(60)
                exports_res = self.t212_api.get_exports()
                dl_link = next(
                    (r.downloadLink for r in exports_res if r.reportId == report_id),
                    None,
                )
                if dl_link:
                    break

        if not dl_link:
            raise Trading212ServiceException(500, "Export not found")

        file_res = requests.get(dl_link, stream=True)

        text_io = StringIO(file_res.text)
        csv_reader = csv.reader(text_io)
        data = list(csv_reader)

        exported_transactions = [
            T212ExportTransaction.from_csv(row) for row in data[1:]
        ]

        return exported_transactions

    def fetch_all_transactions(self, account: BankAccount) -> None:
        exported_transactions = self._get_exported_transactions(
            dt.datetime.now(), dt.datetime.now() - dt.timedelta(weeks=52)
        )

        transactions = self._parse_transactions(account, exported_transactions)

        account.last_synced = dt.datetime.now()
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)
        bank_transaction_repo.add_all(transactions)

        # Import the FinanceService to use the incremental update method
        from lifehub.modules.finance.service.finance_service import FinanceService

        # Only update monthly summary if we have new transactions
        if transactions:
            finance_service = FinanceService(self.session, self.user)
            finance_service._update_monthly_summary_incremental(account, transactions)

        self.session.commit()

    def fetch_new_transactions(self, account: BankAccount) -> None:
        exported_transactions = self._get_exported_transactions(
            dt.datetime.now(), account.last_synced
        )

        transactions = self._parse_transactions(account, exported_transactions)

        account.last_synced = dt.datetime.now()
        bank_transaction_repo = BankTransactionRepository(self.user, self.session)
        bank_transaction_repo.add_all(transactions)

        # Import the FinanceService to use the incremental update method
        from lifehub.modules.finance.service.finance_service import FinanceService

        # Only update monthly summary if we have new transactions
        if transactions:
            finance_service = FinanceService(self.session, self.user)
            finance_service._update_monthly_summary_incremental(account, transactions)

        self.session.commit()
