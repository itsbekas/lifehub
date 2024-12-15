<script lang="ts">
  import * as Dialog from "@/components/ui/dialog";
  import { Button } from "@/components/ui/button";

  export let addCategoryModalVisible = false;

  function closeAddCategoryModal() {
    addCategoryModalVisible = false;
  }
</script>

<Dialog.Root bind:open={addCategoryModalVisible}>
  <Dialog.Trigger>
    <Button class="mb-4">Add a Category</Button>
  </Dialog.Trigger>

  <Dialog.Content class="sm:max-w-[425px]">
    <Dialog.Header>
      <Dialog.Title>Add a New Category</Dialog.Title>
      <Dialog.Description>
        Provide a name for the new category and click "Add Category."
      </Dialog.Description>
    </Dialog.Header>

    <form method="POST" action="?/addCategory">
      <label class="block mb-2">
        Category Name:
        <input
          name="name"
          type="text"
          class="border border-gray-300 rounded-lg w-full p-2 mt-1"
          required
        />
      </label>

      <div class="mt-4 flex justify-end gap-2">
        <Button variant="secondary" type="button" onclick={closeAddCategoryModal}>
          Cancel
        </Button>
        <Button type="submit">Add Category</Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>
