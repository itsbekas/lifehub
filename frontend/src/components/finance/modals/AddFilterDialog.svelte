<script lang="ts">
  import * as Dialog from '@/components/ui/dialog';
  import { Button } from '@/components/ui/button';
  import type { BudgetCategory } from '@/lib/types/finance';

  export let categories: BudgetCategory[] = [];

  let matches: string[] = [''];

  function addMatch() {
    matches = [...matches, ''];
  }

  function removeMatch(index: number) {
    matches = matches.filter((_, i) => i !== index);
  }

</script>

<Dialog.Root>
  <Dialog.Trigger>
    Add Filter
  </Dialog.Trigger>
  <Dialog.Content class="sm:max-w-[425px]">
    <Dialog.Header>
      <Dialog.Title>Add a New Filter</Dialog.Title>
      <Dialog.Description>
        Define a filter to auto-categorize transactions based on matches.
      </Dialog.Description>
    </Dialog.Header>

    <form method="POST" action="?/addFilter">
      <label class="mb-2 block">
        Description:
        <input
          type="text"
          name="description"
          class="mt-1 w-full rounded-lg border border-gray-300 p-2"
          required
        />
      </label>

      <label class="mb-2 block">Matches:</label>
      {#each matches as match, index}
        <div class="mb-2 flex items-center gap-2">
          <input
            type="text"
            bind:value={matches[index]}
            class="w-full rounded-lg border border-gray-300 p-2"
            placeholder="Enter a match"
            required
          />
          {#if matches.length > 1}
            <button
              type="button"
              class="text-red-500 hover:underline"
              onclick={() => removeMatch(index)}
            >
              Remove
            </button>
          {/if}
        </div>
      {/each}
      <button type="button" class="text-blue-500 hover:underline" onclick={addMatch}>
        Add Another Match
      </button>

      <label class="mb-2 mt-4 block">
        Sub-category:
        <select name="subcategoryId" class="mt-1 w-full rounded-lg border border-gray-300 p-2">
          <option value="" disabled selected>Select a sub-category</option>
          {#each categories as category}
            {#each category.subcategories as subcategory}
              <option value={subcategory.id}>{subcategory.name}</option>
            {/each}
          {/each}
        </select>
      </label>

      <input type="hidden" name="matches" value={JSON.stringify(matches)} />

      <div class="mt-4 flex justify-end gap-2">
        <Button type="submit">Add Filter</Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>
