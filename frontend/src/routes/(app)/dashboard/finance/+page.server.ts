import { api_url } from '$lib/api';
import type { BankBalance, BankTransaction } from '$lib/types/finance';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const [balancesRequest, transactionsRequest] = await Promise.all([
        fetch(api_url('/finance/bank/balances')),
        fetch(api_url('/finance/bank/transactions'))
    ]);

    const balancesData: BankBalance[] = await balancesRequest.json();
    const transactionsData: BankTransaction[] = await transactionsRequest.json();

    return { balances: balancesData, transactions: transactionsData };

}
