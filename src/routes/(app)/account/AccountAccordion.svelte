<script lang="ts">
    import { Accordion, AccordionItem, Button, Heading, Listgroup, Modal } from 'flowbite-svelte';

    type AccountAccordionData = {
        title: string;
        category: string;
        cardComponent: any;
        user_items: Array<any>;
        items: Array<any>;
    }

    export let data: AccountAccordionData;

    let showListModal: boolean = false;

</script>

<div id="user-{data.category}-accordion" class="flex flex-col w-full">
    <div id="user-{data.category}-heading" class="flex flex-row m-5 justify-start">
        <Heading tag="h4" class="">{data.title}</Heading>
        <Button on:click={() => (showListModal = true)}>Add {data.title}</Button>
    </div>
    <Accordion>
        {#each data.user_items as item}
        <AccordionItem>
            <span slot="header">{item.name} (ID: {item.id})</span>
            <svelte:component this={data.cardComponent} {item} />
        </AccordionItem>
        {/each}
    </Accordion>
</div>

<Modal size="xs" id="{data.category}-list-modal" bind:open={showListModal} >
    <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Choose a {data.category}</h3>
    <Listgroup items={data.items} let:item>
        <div class="flex flex-row justify-between align-middle h-full">
            {item.name}
            <Button size="xs">Add</Button>
        </div>
    </Listgroup>
</Modal>
