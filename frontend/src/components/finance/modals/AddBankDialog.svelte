<script lang="ts">
  import * as Dialog from "@/components/ui/dialog";
  import { Button } from "@/components/ui/button";
  import type { BankInstitution } from "@/lib/types/finance";

  export let banks: BankInstitution[] = []; // Prop for bank data
  let addBankModalVisible = false;

  function openAddBankModal() {
    addBankModalVisible = true;
  }

  function closeAddBankModal() {
    addBankModalVisible = false;
  }
</script>

<Dialog.Root bind:open={addBankModalVisible}>
  <Dialog.Trigger>
    <button
      class="border border-gray-200 rounded-lg p-4 bg-gray-50 flex items-center justify-center cursor-pointer hover:bg-gray-100 focus:outline-none"
      onclick={openAddBankModal}
    >
      <h3 class="text-md font-medium text-gray-800">Add a Bank</h3>
    </button>
  </Dialog.Trigger>

  <Dialog.Content class="sm:max-w-[425px]">
    <Dialog.Header>
      <Dialog.Title>Add a New Bank</Dialog.Title>
      <Dialog.Description>
        Select a bank from the dropdown and click "Add Bank" to add it to your list.
      </Dialog.Description>
    </Dialog.Header>

    <form method="POST" action="?/addBank">
      <label class="block mb-2">
        Bank Name:
        <select
          name="bankId"
          class="border border-gray-300 rounded-lg w-full p-2 mt-1"
          required
        >
          <option value="" disabled selected>Select a bank</option>
          {#each banks as bank}
            <option value={bank.id}>
              {bank.name}
            </option>
          {/each}
        </select>
      </label>

      <div class="mt-4 flex justify-end gap-2">
        <Button variant="secondary" type="button" onclick={closeAddBankModal}>
          Cancel
        </Button>
        <Button type="submit">Add Bank</Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>
