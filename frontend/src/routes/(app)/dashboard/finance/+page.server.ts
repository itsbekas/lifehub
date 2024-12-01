import { api_url } from '$lib/api';
import type { BankBalance, BankTransaction, BankTransactionFilter, BudgetCategory } from '$lib/types/finance';
import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const [balancesRequest, transactionsRequest, banksRequest, budgetCategoriesRequest, transactionFiltersRequest] = await Promise.all([
        fetch(api_url('/finance/bank/balances')),
        fetch(api_url('/finance/bank/transactions')),
        fetch(api_url('/finance/bank/banks')),
        fetch(api_url('/finance/budget/categories')),
        fetch(api_url('/finance/bank/transactions/filters'))
    ]);

    const balancesData: BankBalance[] = await balancesRequest.json();
    const transactionsData: BankTransaction[] = await transactionsRequest.json();
    const banksData: string[] = await banksRequest.json();
    const budgetCategoriesData: BudgetCategory[] = await budgetCategoriesRequest.json();
    const filtersData: BankTransactionFilter[] = await transactionFiltersRequest.json();

    return {
      balances: balancesData,
      transactions: transactionsData,
      banks: banksData,
      budgetCategories :budgetCategoriesData,
      filters: filtersData, 
    };

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
  addCategory: async ({ request, fetch }) => {
    const formData = await request.formData();
    const name = formData.get('name');

    const response = await fetch(api_url('/finance/budget/categories'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name })
    });
  },
  addSubCategory: async ({ request, fetch }) => {
    const formData = await request.formData();
    const name = formData.get('name');
    const categoryId = formData.get('categoryId');
    const amount = formData.get('amount');

    const response = await fetch(api_url(`/finance/budget/categories/${categoryId}/subcategories`), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, amount })
    });
  },
  editTransaction: async ({ request, fetch }) => {
    const formData = await request.formData();
    const transactionId = formData.get('transactionId');
    const accountId = formData.get('accountId');
    const subcategoryId = formData.get('subcategoryId');
    const amount = formData.get('amount');
    const description = formData.get('description');

    const response = await fetch(api_url(`/finance/bank/${accountId}/transactions/${transactionId}`), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ description, subcategory_id: subcategoryId, amount })
    });
  },
  addFilter: async ({ request, fetch }) => {
    const formData = await request.formData();
    const filter = formData.get('filter');
    const subcategoryId = formData.get('subcategoryId');
    const description = formData.get('description');

    const response = await fetch(api_url('/finance/bank/transactions/filters'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ filter, subcategory_id: subcategoryId, description })
    });
  },
  editFilter: async ({ request, fetch }) => {
    const formData = await request.formData();
    const filterId = formData.get('filterId');
    const filter = formData.get('filter');
    const subcategoryId = formData.get('subcategoryId');
    const description = formData.get('description');

    const response = await fetch(api_url(`/finance/bank/transactions/filters/${filterId}`), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ filter, description, subcategory_id: subcategoryId })
    });
  }
}