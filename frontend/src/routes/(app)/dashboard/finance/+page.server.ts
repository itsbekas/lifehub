import { api_url } from '$lib/api';
import type { BankBalance, BankTransaction } from '$lib/types/finance';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const [balancesRequest, transactionsRequest, banksRequest, budgetCategoriesRequest] = await Promise.all([
        fetch(api_url('/finance/bank/balances')),
        fetch(api_url('/finance/bank/transactions')),
        fetch(api_url('/finance/bank/banks')),
        fetch(api_url('/finance/budget/categories'))
    ]);

    const balancesData: BankBalance[] = await balancesRequest.json();
    const transactionsData: BankTransaction[] = await transactionsRequest.json();
    const banksData: string[] = await banksRequest.json();
    const budgetCategoriesData = await budgetCategoriesRequest.json();

    return { balances: balancesData, transactions: transactionsData, banks: banksData, budgetCategories: budgetCategoriesData };

}
