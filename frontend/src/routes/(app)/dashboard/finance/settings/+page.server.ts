import { api_url } from '$lib/api';
import type { BankTransactionFilter, BudgetCategory } from '$lib/types/finance';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

  const [filtersResponse, categoriesResponse] = await Promise.all([
    fetch(api_url('/finance/bank/transactions/filters')),
    fetch(api_url('/finance/budget/categories'))
  ]);

  const filters: BankTransactionFilter[] = await filtersResponse.json();
  const categories: BudgetCategory[] = await categoriesResponse.json();
  
  return { filters, categories };
}

/** @type {import('./$types').Actions} */
export const actions = {
  addFilter: async ({ request, fetch }) => {
    const formData = await request.formData();
    const subcategoryId = formData.get('subcategoryId');
    const description = formData.get('description');
    const matches = parseMatches(formData.get('matches'));

    await fetch(api_url('/finance/bank/transactions/filters'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subcategory_id: subcategoryId, description, matches })
    });
  },
  editFilter: async ({ request, fetch }) => {
    const formData = await request.formData();
    const filterId = formData.get('filterId');
    const subcategoryId = formData.get('subcategoryId');
    const description = formData.get('description');
    const matches = parseMatches(formData.get('matches'));

    await fetch(api_url(`/finance/bank/transactions/filters/${filterId}`), {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description, subcategory_id: subcategoryId, matches })
    });
  }
};

/**
 * Helper function to parse matches JSON string into an array.
 * @param matchesJson - JSON string containing matches.
 * @returns Parsed array of matches or an empty array.
 */
function parseMatches(matchesJson: FormDataEntryValue | null): string[] {
  if (matchesJson) {
    try {
      return JSON.parse(matchesJson.toString());
    } catch {
      console.error('Failed to parse matches JSON');
    }
  }
  return [];
}
