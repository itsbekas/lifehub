<script lang="ts">
  import * as Card from '@/components/ui/card';

  import AddSubCategoryDialog from './modals/AddSubCategoryDialog.svelte';

  export let category;

  function formatCurrency(amount: number) {
    return `${amount.toFixed(2)}€`;
  }
</script>

<Card.Root>
  <Card.Header>
    <Card.Title>{category.name}</Card.Title>
  </Card.Header>
  <Card.Content>
    <ul class="space-y-2">
      {#each category.subcategories as subcategory}
        <li class="border-b border-gray-200 pb-2">
          <div class="flex justify-between">
            <span>{subcategory.name}</span>
            <span>Budgeted: {formatCurrency(subcategory.budgeted)}</span>
          </div>
          <div class="flex justify-between text-sm text-gray-600">
            <span>Spent: {formatCurrency(subcategory.spent)}</span>
            <span>Available: {formatCurrency(subcategory.available)}</span>
          </div>
        </li>
      {/each}
    </ul>
    <AddSubCategoryDialog categoryId={category.id} />
  </Card.Content>
</Card.Root>
