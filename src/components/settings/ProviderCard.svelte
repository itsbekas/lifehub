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
    <div class="flex justify-between">
    <p class="">{ provider.name }</p>
    <button class="text-red-500" on:click={toggleRemoveModal}>Remove</button>
</SettingsCard>

<Modal title="Remove" bind:isOpen={isRemoveModalOpen}>
    <div class="flex gap-4">
        <p>Are you sure you want to remove { provider.name }?</p>
        <button class="text-red-500" on:click={toggleRemoveModal}>Remove</button>
    </div>
</Modal>
