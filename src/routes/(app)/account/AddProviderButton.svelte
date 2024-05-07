<script lang="ts">

    import { Button, Input, Modal } from 'flowbite-svelte';

    let showModal = false;

    export let data: Provider;

</script>

<Button id="add-{data.name}-provider-button" size="xs" on:click={() => showModal = true}>Add</Button>

<Modal id="add-provider-modal" bind:open={showModal} size="xs" autoclose={false}>
{#if data.type == "oauth"}
    <div id="add-oauth-provider-modal-content">
        <form class="flex flex-col space-y-6" method="POST" action="?/addOAuthProvider">
            <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Sign in to {data.name}</h3>
            <input type="hidden" name="provider_id" value="{data.id}" />
            <Button type="submit" class="w-full1">Login (redirects to {data.name})</Button>
        </form>
    </div>
{:else if data.type == "token"}
    <div id="add-token-provider-modal-content">
        <form class="flex flex-col space-y-6" method="POST" action="?/addTokenProvider">
            <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Add {data.name} token</h3>
            <Input type="hidden" name="provider_id" value="{data.id}" />
            <Input type="text" name="token" placeholder="Token" class="input" />
            <Button type="submit" class="w-full1">Add</Button>
        </form>
    </div>
{:else if data.type == "basic"}
    <div id="add-basic-provider-modal-content">
        <form class="flex flex-col space-y-6" method="POST" action="?/addBasicProvider">
            <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Add {data.name} credentials</h3>
            <Input type="hidden" name="provider_id" value="{data.id}" />
            <Input type="text" name="username" placeholder="Username" class="input" />
            <Input type="password" name="password" placeholder="Password" class="input" />
            <Button type="submit" class="w-full1">Add</Button>
    </div>
{/if}
</Modal>
