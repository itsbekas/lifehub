<script lang="ts">
  import BudgetCategory from '@/components/finance/BudgetCategory.svelte';
  import AddCategoryDialog from '@/components/finance/modals/AddCategoryDialog.svelte';
  import type { BudgetCategory as BudgetCategoryT } from '$lib/types/finance';

  interface Props {
    data: {
      budgetCategories: BudgetCategoryT[];
    };
  }

  let { data }: Props = $props();
</script>

<section>
  <h1 class="mb-4 text-xl font-bold">Budget Overview</h1>
  <AddCategoryDialog />

  <!-- List of Budget Categories -->
  <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
    {#each data.budgetCategories as category (category.id)}
      <BudgetCategory {category} />
    {/each}
  </div>
</section>
