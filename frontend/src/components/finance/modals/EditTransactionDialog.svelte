<script lang="ts">
  import * as Dialog from '@/components/ui/dialog';
  import { Button } from '@/components/ui/button';
  import type { BankTransaction, BudgetCategory } from '@/lib/types/finance';

  export let transaction: BankTransaction | null = null;
  export let categories: BudgetCategory[] = [];
</script>

<Dialog.Root>
  <Dialog.Trigger>Edit</Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title>Edit Transaction</Dialog.Title>
      <Dialog.Description>
        Update the transaction details and click "Save Changes."
      </Dialog.Description>
    </Dialog.Header>

    <form method="POST" action="?/editTransaction">
      <input type="hidden" name="transactionId" value={transaction?.id} />
      <input type="hidden" name="accountId" value={transaction?.account_id} />

      <label class="mb-2 block">
        Description:
        <input
          name="description"
          type="text"
          class="mt-1 w-full rounded-lg border border-gray-300 p-2"
          value={transaction?.user_description || ''}
        />
      </label>
      <label class="mb-2 block">
        Sub-category:
        <select name="subcategoryId" class="mt-1 w-full rounded-lg border border-gray-300 p-2">
          <option value="" disabled selected>Select a sub-category</option>
          {#each categories as category}
            {#each category.subcategories as subcategory}
              <option
                value={subcategory.id}
                selected={subcategory.id === transaction?.subcategory_id}
              >
                {subcategory.name}
              </option>
            {/each}
          {/each}
        </select>
      </label>
      <label class="mb-2 block">
        Amount:
        <input
          name="amount"
          type="number"
          step="0.01"
          class="mt-1 w-full rounded-lg border border-gray-300 p-2"
          value={transaction?.amount || 0}
        />
      </label>

      <div class="mt-4 flex justify-end gap-2">
        <Button type="submit">Save Changes</Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>
