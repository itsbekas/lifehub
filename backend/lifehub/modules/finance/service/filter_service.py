import uuid

from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User
from lifehub.modules.finance.models import (
    BankTransactionFilterRequest,
    BankTransactionFilterResponse,
)
from lifehub.modules.finance.repository import BankTransactionFilterRepository
from lifehub.modules.finance.schema import (
    BankTransactionFilter,
    BankTransactionFilterMatch,
)
from lifehub.modules.finance.service.finance_service import FinanceServiceException


class FilterServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Filter", status_code, message)


class FilterService(BaseUserService):
    _encryption_service: EncryptionService | None = None

    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    @property
    def encryption_service(self) -> EncryptionService:
        if self._encryption_service is None:
            self._encryption_service = EncryptionService(self.session, self.user)
        return self._encryption_service

    def get_bank_transactions_filters(self) -> list[BankTransactionFilterResponse]:
        bank_transaction_filters_repo = BankTransactionFilterRepository(
            self.user, self.session
        )
        return [
            BankTransactionFilterResponse(
                id=str(filter.id),
                description=filter.description,
                subcategory_id=str(filter.subcategory_id),
                matches=[match.match_string for match in filter.matches],
            )
            for filter in bank_transaction_filters_repo.get_all()
        ]

    def create_bank_transactions_filter(
        self, data: BankTransactionFilterRequest
    ) -> BankTransactionFilterResponse:
        bank_transaction_filters_repo = BankTransactionFilterRepository(
            self.user, self.session
        )
        filter = BankTransactionFilter(
            user_id=self.user.id,
            description=data.description if data.description else None,
            subcategory_id=uuid.UUID(data.subcategory_id)
            if data.subcategory_id
            else None,
            matches=[],
        )

        # Handle the case where matches is None
        if data.matches is not None:
            filter.matches = [
                BankTransactionFilterMatch(filter_id=filter.id, match_string=match)
                for match in data.matches
            ]

        bank_transaction_filters_repo.add(filter)

        self.session.commit()
        return BankTransactionFilterResponse(
            id=str(filter.id),
            description=filter.description,
            subcategory_id=str(filter.subcategory_id)
            if filter.subcategory_id
            else None,
            matches=[match.match_string for match in filter.matches],
        )

    def update_bank_transactions_filter(
        self, filter_id: uuid.UUID, data: BankTransactionFilterRequest
    ) -> BankTransactionFilterResponse:
        bank_transaction_filters_repo = BankTransactionFilterRepository(
            self.user, self.session
        )
        filter = bank_transaction_filters_repo.get_by_id(filter_id)
        if filter is None:
            raise FinanceServiceException(404, "Filter not found")
        filter.description = (
            data.description if data.description else filter.description
        )
        filter.subcategory_id = (
            uuid.UUID(data.subcategory_id)
            if data.subcategory_id
            else filter.subcategory_id
        )

        # Update matches explicitly
        existing_matches = {match.match_string for match in filter.matches}
        new_matches = set(data.matches or [])

        # Add new matches
        for match_string in new_matches - existing_matches:
            filter.matches.append(
                BankTransactionFilterMatch(
                    filter_id=filter.id, match_string=match_string
                )
            )

        # Remove old matches explicitly
        matches_to_remove = [
            match for match in filter.matches if match.match_string not in new_matches
        ]
        for match in matches_to_remove:
            self.session.delete(match)  # Explicitly delete match from the session

        self.session.commit()

        return BankTransactionFilterResponse(
            id=str(filter.id),
            description=filter.description,
            subcategory_id=str(filter.subcategory_id)
            if filter.subcategory_id
            else None,
            matches=[match.match_string for match in filter.matches],
        )
