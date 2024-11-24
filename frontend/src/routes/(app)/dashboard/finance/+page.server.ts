import { api_url } from '$lib/api';
import type { BankBalance, BankTransaction } from '$lib/types/finance';
import { redirect } from '@sveltejs/kit';

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

/** @type {import('./$types').Actions} */
export const actions = {
  addBank: async ({ request, fetch }) => {
    const formData = await request.formData();
    const bank_id = formData.get('bankId');

    if (!bank_id) {
      return {
        status: 400,
        errors: { bank_id: 'Bank ID is required' }
      };
    }
    
    let url;

    try {
      const response = await fetch(api_url(`/finance/bank/login?bank_id=${bank_id}`));

      if (!response.ok) {
        return {
          status: response.status,
          errors: { general: 'Failed to fetch the login URL' }
        };
      }

      url = await response.json();

    } catch (error) {
      return {
        status: 500,
        errors: { general: 'An error occurred while processing your request' }
      };
    }

    if (url) {
      throw redirect(303, url);
    } else {
      return {
        status: 500,
        errors: { general: 'Invalid response from server' }
      };
    }
  },
  addCategory: async ({ request, fetch }) => {
    const formData = await request.formData();
    const name = formData.get('name');

    if (!name) {
      return {
        status: 400,
        errors: { name: 'Name is required' }
      };
    }

    try {
      const response = await fetch(api_url('/finance/budget/categories'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
      });

      if (!response.ok) {
        return {
          status: response.status,
          errors: { general: 'Failed to add the category' }
        };
      }

    } catch (error) {
      return {
        status: 500,
        errors: { general: 'An error occurred while processing your request' }
      };
    }

    return {
      status: 200,
      message: 'Category added successfully'
    };
  }
};
