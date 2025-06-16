import csv
import datetime as dt
import time
from io import StringIO
from typing import Any

import requests
from sqlalchemy.orm import Session

from lifehub.core.common.base.api_client import APIException
from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User
from lifehub.providers.trading212.api_client import Trading212APIClient

from ..models import T212ExportTransaction
from ..schema import BankAccount, BankTransaction


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

    def fetch_balance(self) -> float:
        """
        Fetches the latest balance from Trading212.
        """
        return Trading212APIClient(self.user, self.session).get_account_cash().free

    def _parse_transactions(
        self, account: BankAccount, t212_transactions: list[T212ExportTransaction]
    ) -> list[BankTransaction]:
        transactions = []

        for t in t212_transactions:
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

            encrypted_description = self.encryption_service.encrypt_data(
                description if description is not None else ""
            )
            encrypted_counterparty = self.encryption_service.encrypt_data(
                counterparty if counterparty is not None else ""
            )
            encrypted_amount = self.encryption_service.encrypt_data(str(amount))

            new_t = BankTransaction(
                transaction_id=t.id,
                account_id=account.id,
                date=dt.datetime.fromisoformat(t.time),
                amount=encrypted_amount,
                description=encrypted_description,
                counterparty=encrypted_counterparty,
            )

            transactions.append(new_t)

        return transactions

    def _read_export_csv(self, csv_data: str) -> list[T212ExportTransaction]:
        """
        Normalizes the CSV data from Trading212 export to a list of T212ExportTransaction.
        """
        text_io = StringIO(csv_data)
        csv_reader = csv.DictReader(text_io)

        exported_transactions = []

        row: dict[str, Any]
        for row in csv_reader:
            # Convert '' to None
            for key, value in row.items():
                if value == "":
                    row[key] = None
            exported_transactions.append(T212ExportTransaction(**row))

        return exported_transactions

    def _get_export_url(self, from_date: dt.datetime, to_date: dt.datetime) -> str:
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
            time.sleep(10)  # Wait for the export to be generated
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

        return dl_link

    def _get_exported_transactions(
        self, to_date: dt.datetime, from_date: dt.datetime
    ) -> list[T212ExportTransaction]:
        dl_link = self._get_export_url(from_date, to_date)
        file_res = requests.get(dl_link, stream=True)
        return self._read_export_csv(file_res.text)

    def fetch_new_transactions(self, account: BankAccount) -> None:
        exported_transactions = self._get_exported_transactions(
            dt.datetime.now(), account.last_synced
        )

        transactions = self._parse_transactions(account, exported_transactions)
        account.last_synced = dt.datetime.now()

        self.session.add_all(transactions)
        self.session.commit()

    def fetch_all_transactions(self, account: BankAccount) -> None:
        # TODO: Eventually this might also be used to get transactions older than a year
        exported_transactions = self._get_exported_transactions(
            dt.datetime.now(), dt.datetime.now() - dt.timedelta(weeks=52)
        )

        transactions = self._parse_transactions(account, exported_transactions)
        account.last_synced = dt.datetime.now()

        self.session.add_all(transactions)
        self.session.commit()
