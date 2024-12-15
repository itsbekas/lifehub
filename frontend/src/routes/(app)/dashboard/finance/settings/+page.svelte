<script lang="ts">
  import AddFilterDialog from '@/components/finance/modals/AddFilterDialog.svelte';
import type { BankTransactionFilter, BudgetCategory } from '@/lib/types/finance';

  interface Props {
    data: {
      filters: BankTransactionFilter[];
      categories: BudgetCategory[];
    };
  }
  
  let { data }: Props = $props();
</script>

<section>
  <h1 class="mb-4 text-xl font-bold">Settings</h1>
  <h2 class="text-lg font-semibold">Manage Filters</h2>
  <p>Create filters to auto-categorize transactions.</p>

  <!-- Filters List -->
  <div class="filters mt-4">
    {#each data.filters as filter (filter.id)}
      <div class="mb-4 rounded-lg border bg-white p-4">
        <h3 class="font-medium">{filter.description}</h3>
        <p>Matches: {filter.matches.join(', ')}</p>
      </div>
    {/each}
  </div>
  <AddFilterDialog categories={ data.categories }/>
</section>
