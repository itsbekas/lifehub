export interface BankBalance {
    bank: string;
    balance: number;
}

export interface BankTransaction {
    transaction_id: string;
    account_id: string;
    amount: number;
    date: string;
    description: string | null;
    counterparty: string | null;
}

export interface BudgetSubCategory {
    id: string;
    name: string;
    category_id: string;
    category_name: string;
    budgeted: number;
    spent: number;
    available: number;
}

export interface BudgetCategory {
    id: string;
    name: string;
    subcategories: BudgetSubCategory[];
}