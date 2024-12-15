<script lang="ts">
  import { enhance } from '$app/forms';
  import SettingsCard from '@/components/settings/SettingsCard.svelte';
  import Modal from '@/components/Modal.svelte';

  interface Props {
    provider: Provider;
  }

  let { provider }: Props = $props();

  let isRemoveModalOpen = $state(false);
  let canConnect: boolean = $state();

  function toggleRemoveModal() {
    isRemoveModalOpen = !isRemoveModalOpen;
  }
</script>

<SettingsCard>
  <div class="flex justify-between gap-4">
    <p class="">{provider.name}</p>
    <div class="flex gap-4">
      {#if canConnect === undefined}
        <form
          method="POST"
          action="?/testProvider"
          use:enhance={({}) => {
            return async ({ result }) => {
              if (result.type === 'success') {
                canConnect = true;
              } else {
                canConnect = false;
              }
            };
          }}
        >
          <input type="hidden" name="provider_id" value={provider.id} />
          <input type="hidden" name="type" value={provider.type} />
          <button type="submit">Test</button>
        </form>
      {:else if canConnect === false}
        <p class="text-red-500">Failed</p>
      {:else if canConnect === true}
        <p class="text-green-500">Connected</p>
      {/if}
      <button class="text-red-500" onclick={toggleRemoveModal}>Remove</button>
    </div>
  </div></SettingsCard
>

<Modal title="Remove" bind:isOpen={isRemoveModalOpen}>
  <div class="flex gap-4">
    <form method="POST" action="?/removeProvider">
      <p>Are you sure you want to remove {provider.name}?</p>
      <input type="hidden" name="provider_id" value={provider.id} />
      <input type="hidden" name="type" value={provider.type} />
      <button type="submit" class="w-full">Remove</button>
    </form>
  </div>
</Modal>
