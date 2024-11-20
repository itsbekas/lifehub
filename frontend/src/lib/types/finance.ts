export interface BankBalance {
    bank: string;
    balance: number;
}

export interface BankTransaction {
    transaction_id: string;
    account_id: string;
    amount: number;
    date: string | null;
    description: string | null;
    counterparty: string | null;
}