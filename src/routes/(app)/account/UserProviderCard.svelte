<script lang="ts">

    import { Button, Heading, Li, List, Modal } from 'flowbite-svelte';

    export let item: Provider;

    let showDeleteModal = false;

</script>

<div id="provider-card-{item.id}" class="flex flex-row justify-between gap-4">
    <div class="flex gap-4">
        <Button>Modify Authentication</Button>
        <Button color="red" on:click={() => showDeleteModal = true}>Delete</Button>
    </div>
    <div class="flex flex-row mr-4 gap-4">
        <Heading tag="h2" customSize="text-lg font-semibold">Required by:</Heading>
        <List tag="ul" list="none">
            {#each item.modules as module}
                <Li>{module.name}</Li>
            {/each}
        </List>
    </div>
</div>

<Modal bind:open={showDeleteModal}>
    <p>Are you sure you want to delete this provider?</p>
    <form method="POST" action="?/deleteProvider">
        <input type="hidden" name="provider_id" value="{item.id}" />
        <div class="flex flex-row gap-4 justify-end">
            <Button color="red" type="submit">Delete</Button>
            <Button on:click={() => showDeleteModal = false}>Cancel</Button>
        </div>
    </form>
</Modal>
