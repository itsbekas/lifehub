<script lang="ts">

    import { Button, Heading, Li, List } from 'flowbite-svelte';

    export let provider: Provider;
</script>

<div id="provider-card-{provider.id}" class="flex flex-row justify-between gap-4">
    <div class="flex gap-4">
        <Button>Modify Authentication</Button>
        <Button color="red">Delete</Button>
    </div>
    <div class="flex flex-row mr-4 gap-4">
        <Heading tag="h2" customSize="text-lg font-semibold">Required by:</Heading>
        <List tag="ul" list="none">
            {#each provider.modules as module}
                <Li>{module.name}</Li>
            {/each}
        </List>
    </div>
</div>
