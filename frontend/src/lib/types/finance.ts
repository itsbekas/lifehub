export interface BankBalance {
    bank: string;
    account_id: string;
    balance: number;
}

export interface BankTransaction {
    id: string;
    account_id: string;
    amount: number;
    date: string;
    description: string | null;
    counterparty: string | null;
    user_description: string | null;
    subcategory_id: string | null;
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

export interface BankInstitution {
    id: string;
    name: string;
    logo: string;
}

export interface BankTransactionFilter {
    id: string;
    filter: string;
    subcategory_id: string | null;
    description: string | null;
}
