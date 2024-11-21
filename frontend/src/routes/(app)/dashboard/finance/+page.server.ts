import { api_url } from '$lib/api';
import type { BankBalance, BankTransaction } from '$lib/types/finance';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const [balancesRequest, transactionsRequest, banksRequest] = await Promise.all([
        fetch(api_url('/finance/bank/balances')),
        fetch(api_url('/finance/bank/transactions')),
        fetch(api_url('/finance/bank/banks'))
    ]);

    const balancesData: BankBalance[] = await balancesRequest.json();
    const transactionsData: BankTransaction[] = await transactionsRequest.json();
    const banksData: string[] = await banksRequest.json();

    return { balances: balancesData, transactions: transactionsData, banks: banksData };

}
