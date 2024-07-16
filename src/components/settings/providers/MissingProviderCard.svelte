<script lang="ts">
    import SettingsCard from '$components/settings/SettingsCard.svelte';
    import Modal from '$components/Modal.svelte';

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
            <div class="flex flex-row">
                <input type="hidden" name="provider_id" value="{provider.id}" />
                <input type="text" name="username" placeholder="Username" class="input" />
                <input type="password" name="password" placeholder="Password" class="input" />
                {#if provider.allow_custom_url}
                    <input type="text" name="custom_url" placeholder="URL" class="input" />
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
            <div class="flex flex-row">
                <input type="hidden" name="provider_id" value="{provider.id}" />
                <input type="text" name="token" placeholder="Token" class="input" />
                {#if provider.allow_custom_url}
                    <input type="text" name="custom_url" placeholder="URL" class="input" />
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
