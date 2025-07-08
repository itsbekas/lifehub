import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from lifehub.core.common.base.service.user import BaseUserService
from lifehub.core.common.exceptions import ServiceException
from lifehub.core.security.encryption import EncryptionService
from lifehub.core.user.schema import User

from ..models import BudgetCategoryResponse, BudgetSubCategoryResponse
from ..repository import BudgetCategoryRepository, BudgetSubCategoryRepository
from ..schema import BudgetCategory, BudgetSubCategory, BudgetSubCategoryType


class BudgetServiceException(ServiceException):
    def __init__(self, status_code: int, message: str):
        super().__init__("Budget", status_code, message)


class BudgetService(BaseUserService):
    _encryption_service: EncryptionService | None = None

    def __init__(self, session: Session, user: User):
        super().__init__(session, user)

    @property
    def encryption_service(self) -> EncryptionService:
        if self._encryption_service is None:
            self._encryption_service = EncryptionService(self.session, self.user)
        return self._encryption_service

    def _get_budget_status(
        self, subcategory_id: uuid.UUID
    ) -> tuple[float, float, float]:
        """
        Fetches the budgeted, spent, and available amounts for a specific subcategory.
        """
        subcategory = BudgetSubCategoryRepository(self.session).get_by_id(
            subcategory_id
        )

        if subcategory is None:
            raise BudgetServiceException(404, "Subcategory not found")

        # Fetch budgeted amount
        budgeted = float(self.encryption_service.decrypt_data(subcategory.amount))

        spent = 0  # TODO: Get monthly spent

        # Calculate available amount
        available = budgeted - spent
        return round(budgeted, 2), round(spent, 2), round(available, 2)

    def get_budget_categories(self) -> list[BudgetCategoryResponse]:
        """
        Fetches the budget categories and subcategories, dynamically calculating the budgeted, spent, and available amounts.
        """
        categories = []
        for category in self.user.budget_categories:
            subcategories = []
            for subcategory in category.subcategories:
                budgeted, spent, available = self._get_budget_status(subcategory.id)

                subcategories.append(
                    BudgetSubCategoryResponse(
                        id=str(subcategory.id),
                        name=self.encryption_service.decrypt_data(subcategory.name),
                        category_id=str(category.id),
                        category_name=self.encryption_service.decrypt_data(
                            category.name
                        ),
                        budgeted=budgeted,
                        spent=spent,
                        available=available,
                    )
                )
            categories.append(
                BudgetCategoryResponse(
                    id=str(category.id),
                    name=self.encryption_service.decrypt_data(category.name),
                    subcategories=subcategories,
                )
            )
        return categories

    def create_budget_category(self, name: str) -> BudgetCategoryResponse:
        """
        Creates a new budget category.
        """
        category = BudgetCategory(
            user_id=self.user.id,
            name=self.encryption_service.encrypt_data(name),
        )
        self.user.budget_categories.append(category)
        self.session.commit()
        return BudgetCategoryResponse(
            id=str(category.id),
            name=self.encryption_service.decrypt_data(category.name),
            subcategories=[],
        )

    def get_budget_category(self, category_id: uuid.UUID) -> BudgetCategoryResponse:
        """
        Fetches a budget category by ID, dynamically calculating the budgeted, spent, and available amounts for each subcategory.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise BudgetServiceException(404, "Category not found")

        subcategories = []
        for subcategory in category.subcategories:
            budgeted, spent, available = self._get_budget_status(subcategory.id)

            subcategories.append(
                BudgetSubCategoryResponse(
                    id=str(subcategory.id),
                    name=self.encryption_service.decrypt_data(subcategory.name),
                    category_id=str(category.id),
                    category_name=self.encryption_service.decrypt_data(category.name),
                    budgeted=budgeted,
                    spent=spent,
                    available=available,
                )
            )

        return BudgetCategoryResponse(
            id=str(category.id),
            name=self.encryption_service.decrypt_data(category.name),
            subcategories=subcategories,
        )

    def update_budget_category(
        self, category_id: uuid.UUID, name: str
    ) -> BudgetCategoryResponse:
        """
        Updates a budget category by ID.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise BudgetServiceException(404, "Category not found")
        category.name = self.encryption_service.encrypt_data(name)
        self.session.commit()
        return BudgetCategoryResponse(id=str(category.id), name=name, subcategories=[])

    def delete_budget_category(self, category_id: uuid.UUID) -> None:
        """
        Deletes a budget category by ID.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise BudgetServiceException(404, "Category not found")
        self.session.delete(category)
        self.session.commit()

    def get_budget_subcategories(
        self, category_id: uuid.UUID
    ) -> list[BudgetSubCategoryResponse]:
        """
        Fetches the subcategories of a budget category, dynamically calculating the budgeted, spent, and available amounts.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise BudgetServiceException(404, "Category not found")

        subcategories = []
        for subcategory in category.subcategories:
            budgeted, spent, available = self._get_budget_status(subcategory.id)

            subcategories.append(
                BudgetSubCategoryResponse(
                    id=str(subcategory.id),
                    name=self.encryption_service.decrypt_data(subcategory.name),
                    category_id=str(category.id),
                    category_name=self.encryption_service.decrypt_data(category.name),
                    budgeted=budgeted,
                    spent=spent,
                    available=available,
                )
            )
        return subcategories

    def create_budget_subcategory(
        self, category_id: uuid.UUID, name: str, amount: float, type: BudgetSubCategoryType
    ) -> BudgetSubCategoryResponse:
        """
        Creates a new budget subcategory with the specified budgeted amount.
        """
        category = BudgetCategoryRepository(self.user, self.session).get_by_id(
            category_id
        )
        if category is None:
            raise BudgetServiceException(404, "Category not found")

        subcategory = BudgetSubCategory(
            category_id=category.id,
            name=self.encryption_service.encrypt_data(name),
            amount=self.encryption_service.encrypt_data(str(Decimal(amount))),
            type=type,
        )
        category.subcategories.append(subcategory)
        self.session.commit()

        # Fetch budgeted amount
        budgeted = float(self.encryption_service.decrypt_data(subcategory.amount))

        # Initially, there are no transactions, so spent is 0 and available equals the budgeted amount
        spent = 0.0
        available = budgeted - spent

        return BudgetSubCategoryResponse(
            id=str(subcategory.id),
            name=self.encryption_service.decrypt_data(subcategory.name),
            category_id=str(category.id),
            category_name=self.encryption_service.decrypt_data(category.name),
            budgeted=budgeted,
            spent=spent,
            available=available,
        )

    def update_budget_subcategory(
        self, subcategory_id: uuid.UUID, name: str, amount: float
    ) -> BudgetSubCategoryResponse:
        """
        Updates a budget subcategory by ID.
        """
        subcategory = BudgetSubCategoryRepository(self.session).get_by_id(
            subcategory_id
        )
        if subcategory is None:
            raise BudgetServiceException(404, "Subcategory not found")
        subcategory.name = self.encryption_service.encrypt_data(name)
        subcategory.amount = self.encryption_service.encrypt_data(str(Decimal(amount)))
        self.session.commit()

        budgeted, spent, available = self._get_budget_status(subcategory.id)

        return BudgetSubCategoryResponse(
            id=str(subcategory.id),
            name=self.encryption_service.decrypt_data(subcategory.name),
            category_id=str(subcategory.category_id),
            category_name=self.encryption_service.decrypt_data(
                subcategory.category.name
            ),
            budgeted=budgeted,
            spent=spent,
            available=available,
        )

    def delete_budget_subcategory(self, subcategory_id: uuid.UUID) -> None:
        """
        Deletes a budget subcategory by ID.
        """
        subcategory = BudgetSubCategoryRepository(self.session).get_by_id(
            subcategory_id
        )
        if subcategory is None:
            raise BudgetServiceException(404, "Subcategory not found")
        self.session.delete(subcategory)
        self.session.commit()
