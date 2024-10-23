<script lang="ts">
    import SettingsCard from '$components/settings/SettingsCard.svelte';
    import Modal from '$components/Modal.svelte';
    import TextInput from '$components/TextInput.svelte';

    export let provider: Provider;

    let isAddModalOpen = {
        basic: false,
        token: false,
        oauth: false
    };

    function toggleAddModal(provider: Provider) {
        isAddModalOpen.basic = false;
        isAddModalOpen.token = false;
        isAddModalOpen.oauth = false;

        switch (provider.type) {
            case 'basic':
                isAddModalOpen.basic = true;
                break;
            case 'token':
                isAddModalOpen.token = true;
                break;
            case 'oauth':
                isAddModalOpen.oauth = true;
                break;
        }
    }

</script>

<SettingsCard>
    <div class="flex justify-between gap-4">
    <p class="">{ provider.name }</p>
    <button class="text-blue-500" on:click={() => toggleAddModal(provider)}>Add</button>
</SettingsCard>

<!-- Basic Provider (User/Password) -->
<Modal title="Add Basic Provider" bind:isOpen={(isAddModalOpen.basic)}>
    <div class="flex gap-4">
        <form method="POST" action="?/addBasicProvider">
            <div class="flex flex-col">
                <input type="hidden" name="provider_id" value="{provider.id}" />
                <TextInput type="text" name="username" placeholder="Username" />
                <TextInput type="password" name="password" placeholder="Password" />
                {#if provider.allow_custom_url}
                    <TextInput type="text" name="custom_url" placeholder="URL" />
                {/if}
                <button type="submit" class="w-full">Add</button>
            </div>
        </form>
    </div>
</Modal>

<!-- Token Provider -->
<Modal title="Add Token Provider" bind:isOpen={isAddModalOpen.token}>
    <div class="flex gap-4">
        <form method="POST" action="?/addTokenProvider">
            <div class="flex flex-col">
                <input type="hidden" name="provider_id" value="{provider.id}" />
                <TextInput name="token" placeholder="Token" />
                {#if provider.allow_custom_url}
                    <TextInput type="text" name="custom_url" placeholder="URL" />
                {/if}
                <button type="submit" class="w-full">Add</button>
            </div>
        </form>
    </div>
</Modal>

<!-- OAuth Provider -->
<Modal title="Add OAuth Provider" bind:isOpen={isAddModalOpen.oauth}>
    <div class="flex gap-4">
        <form method="POST" action="?/addOAuthProvider">
            <div class="flex flex-row">
                <input type="hidden" name="provider_id" value="{provider.id}" />
                <button type="submit" class="w-full">Login (redirects to {provider.name})</button>
            </div>
        </form>
    </div>
</Modal>
