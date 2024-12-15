import { api_url } from '$lib/api';
import type { BankBalance, BankTransaction, BudgetCategory } from '$lib/types/finance';
import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
  const [balancesResponse, transactionsResponse, budgetCategoriesResponse] = await Promise.all([
    fetch(api_url('/finance/bank/balances')),
    fetch(api_url('/finance/bank/transactions')),
    fetch(api_url('/finance/budget/categories'))
  ]);

  const balances: BankBalance[] = await balancesResponse.json();
  const transactions: BankTransaction[] = await transactionsResponse.json();
  const budgetCategories: BudgetCategory[] = await budgetCategoriesResponse.json();

  return { balances, transactions, budgetCategories };
}

/** @type {import('./$types').Actions} */
export const actions = {
  addBank: async ({ request, fetch }) => {
    const formData = await request.formData();
    const bankId = formData.get('bankId');

    const response = await fetch(api_url(`/finance/bank/login?bank_id=${bankId}`));
    const url = await response.json();

    throw redirect(303, url);
  },
  editTransaction: async ({ request, fetch }) => {
    const formData = await request.formData();
    const transactionId = formData.get('transactionId');
    const accountId = formData.get('accountId');
    const subcategoryId = formData.get('subcategoryId');
    const amount = formData.get('amount');
    const description = formData.get('description');

    await fetch(api_url(`/finance/bank/${accountId}/transactions/${transactionId}`), {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description, subcategory_id: subcategoryId, amount })
    });
  }
};
