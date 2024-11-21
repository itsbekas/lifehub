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