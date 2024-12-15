<script lang="ts">
  import * as Dialog from '@/components/ui/dialog';
  import { Button } from "@/components/ui/button";

  export let categoryId: string | null = null;
</script>

<Dialog.Root>
  <Dialog.Trigger>
    <Button>Add a Sub-category</Button>
  </Dialog.Trigger>

  <Dialog.Content class="sm:max-w-[425px]">
    <Dialog.Header>
      <Dialog.Title>Add a New Sub-category</Dialog.Title>
      <Dialog.Description>
        Provide details for the new sub-category and click "Add Sub-category."
      </Dialog.Description>
    </Dialog.Header>

    <form method="POST" action="?/addSubCategory">
      <input type="hidden" name="categoryId" value={categoryId} />
      <label class="mb-2 block">
        Sub-category Name:
        <input
          name="name"
          type="text"
          class="mt-1 w-full rounded-lg border border-gray-300 p-2"
          required
        />
      </label>
      <label class="mb-2 block">
        Budgeted Amount:
        <input
          name="amount"
          type="number"
          step="0.01"
          class="mt-1 w-full rounded-lg border border-gray-300 p-2"
          required
        />
      </label>

      <div class="mt-4 flex justify-end gap-2">
        <Button type="submit">Add Sub-category</Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>
