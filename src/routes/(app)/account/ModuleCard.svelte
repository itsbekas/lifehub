<script lang="ts">

    import { Button, Heading, Li, List } from 'flowbite-svelte';

    export let module: Module;
</script>

<div id="provider-card-{module.id}" class="flex flex-row justify-between gap-4">
    <div class="flex gap-4">
        <Button color="red">Delete</Button>
    </div>
    <div class="flex flex-row mr-4 gap-4">
        <Heading tag="h2" customSize="text-lg font-semibold">Requires:</Heading>
        <List tag="ul" list="none">
            {#each module.providers as provider}
                <Li>{provider.name}</Li>
            {/each}
        </List>
    </div>
</div>
