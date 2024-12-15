import { api_url } from '$lib/api';
import type { BudgetCategory } from '$lib/types/finance';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
  const response = await fetch(api_url('/finance/budget/categories'));
  const budgetCategories: BudgetCategory[] = await response.json();

  return { budgetCategories };
}

/** @type {import('./$types').Actions} */
export const actions = {
  addCategory: async ({ request, fetch }) => {
    const formData = await request.formData();
    const name = formData.get('name');

    await fetch(api_url('/finance/budget/categories'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
  },
  addSubCategory: async ({ request, fetch }) => {
    const formData = await request.formData();
    const name = formData.get('name');
    const categoryId = formData.get('categoryId');
    const amount = formData.get('amount');

    await fetch(api_url(`/finance/budget/categories/${categoryId}/subcategories`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, amount })
    });
  }
};
