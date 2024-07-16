<script lang="ts">
    import SettingsCard from '$components/settings/SettingsCard.svelte';
    import Modal from '$components/Modal.svelte';

    export let provider: Provider;

    let isRemoveModalOpen = false;

    function toggleRemoveModal() {
        isRemoveModalOpen = !isRemoveModalOpen;
    }
</script>

<SettingsCard>
    <div class="flex justify-between gap-4">
    <p class="">{ provider.name }</p>
    <button class="text-red-500" on:click={toggleRemoveModal}>Remove</button>
</SettingsCard>

<Modal title="Remove" bind:isOpen={isRemoveModalOpen}>
    <div class="flex gap-4">
        <form method="POST" action="?/removeProvider">
            <p>Are you sure you want to remove { provider.name }?</p>
            <input type="hidden" name="provider_id" value="{provider.id}" />
            <input type="hidden" name="type" value="{provider.type}" />
            <button type="submit" class="w-full">Remove</button>
        </form>
    </div>
</Modal>
