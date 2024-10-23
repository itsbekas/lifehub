from __future__ import annotations

from typing import Any


class Account:
    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        on_budget: bool,
        closed: bool,
        note: str | None,
        balance: int,
        cleared_balance: int,
        uncleared_balance: int,
        transfer_payee_id: str | None,
        direct_import_linked: bool | None,
        direct_import_in_error: bool | None,
        last_reconciled_at: str | None,
        debt_original_balance: int | None,
        debt_interest_rates: dict[str, Any] | None,
        debt_minimum_payments: dict[str, Any] | None,
        debt_escrow_amounts: dict[str, Any] | None,
        deleted: bool,
    ) -> None:
        self.id: str = id
        self.name: str = name
        self.type: str = type
        self.on_budget: bool = on_budget
        self.closed: bool = closed
        self.note: str | None = note
        self.balance: int = balance // 1000
        self.cleared_balance: int = cleared_balance // 1000
        self.uncleared_balance: int = uncleared_balance // 1000
        self.transfer_payee_id: str | None = transfer_payee_id
        self.direct_import_linked: bool | None = direct_import_linked
        self.direct_import_in_error: bool | None = direct_import_in_error
        self.last_reconciled_at: str | None = last_reconciled_at
        self.debt_original_balance: int | None = debt_original_balance
        self.debt_interest_rates: dict[str, Any] | None = debt_interest_rates
        self.debt_minimum_payments: dict[str, Any] | None = debt_minimum_payments
        self.debt_escrow_amounts: dict[str, Any] | None = debt_escrow_amounts
        self.deleted: bool = deleted

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Account:
        return cls(**data)

    def __repr__(self) -> str:
        return f"<YNAB Account: {self.name}>"


class Category:
    def __init__(
        self,
        id: str,
        category_group_id: str,
        category_group_name: str,
        name: str,
        hidden: bool,
        note: str | None,
        budgeted: int,
        activity: int,
        balance: int,
        goal_type: str | None,
        goal_day: int | None,
        goal_cadence: int | None,
        goal_cadence_frequency: int | None,
        goal_creation_month: str | None,
        goal_target: int | None,
        goal_target_month: str | None,
        goal_percentage_complete: int | None,
        goal_months_to_budget: int | None,
        goal_under_funded: int | None,
        goal_overall_funded: int | None,
        goal_overall_left: int | None,
        deleted: bool,
        original_category_group_id: str | None = None,  # deprecated
    ) -> None:
        self.id: str = id
        self.category_group_id: str = category_group_id
        self.category_group_name: str = category_group_name
        self.name: str = name
        self.hidden: bool = hidden
        self.note: str | None = note
        self.budgeted: int = budgeted // 1000
        self.activity: int = activity // 1000
        self.balance: int = balance // 1000
        self.goal_type: str | None = goal_type
        self.goal_day: int | None = goal_day
        self.goal_cadence: int | None = goal_cadence
        self.goal_cadence_frequency: int | None = goal_cadence_frequency
        self.goal_creation_month: str | None = goal_creation_month
        self.goal_target: int | None = goal_target
        self.goal_target_month: str | None = goal_target_month
        self.goal_percentage_complete: int | None = goal_percentage_complete
        self.goal_months_to_budget: int | None = goal_months_to_budget
        self.goal_under_funded: int | None = goal_under_funded
        self.goal_overall_funded: int | None = goal_overall_funded
        self.goal_overall_left: int | None = goal_overall_left
        self.deleted: bool = deleted

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Category:
        return cls(**data)

    def __repr__(self) -> str:
        return f"<YNAB Category: {self.name}>"


class CategoryGroup:
    def __init__(
        self,
        id: str,
        name: str,
        hidden: bool,
        deleted: bool,
        categories: list[dict[str, Any]],
    ) -> None:
        self.id: str = id
        self.name: str = name
        self.hidden: bool = hidden
        self.deleted: bool = deleted
        self.categories: list[Category] = [
            Category.from_response(c) for c in categories
        ]

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> CategoryGroup:
        return cls(**data)

    def __repr__(self) -> str:
        return f"<YNAB CategoryGroup: {self.name} ({len(self.categories)} categories)>"


class LoanAccountPeriodicValue:
    pass
