<script lang="ts">
  import * as Dialog from '@/components/ui/dialog';
  import { Button } from '@/components/ui/button';
  import type { BankInstitution } from '@/lib/types/finance';

  export let banks: BankInstitution[] = []; // Prop for bank data
</script>

<Dialog.Root>
  <Dialog.Trigger>Add a bank</Dialog.Trigger>

  <Dialog.Content class="sm:max-w-[425px]">
    <Dialog.Header>
      <Dialog.Title>Add a New Bank</Dialog.Title>
      <Dialog.Description>
        Select a bank from the dropdown and click "Add Bank" to add it to your list.
      </Dialog.Description>
    </Dialog.Header>

    <form method="POST" action="?/addBank">
      <label class="mb-2 block">
        Bank Name:
        <select name="bankId" class="mt-1 w-full rounded-lg border border-gray-300 p-2" required>
          <option value="" disabled selected>Select a bank</option>
          {#each banks as bank}
            <option value={bank.id}>
              {bank.name}
            </option>
          {/each}
        </select>
      </label>

      <div class="mt-4">
        <Button type="submit">Add Bank</Button>
      </div>
    </form>
  </Dialog.Content>
</Dialog.Root>
