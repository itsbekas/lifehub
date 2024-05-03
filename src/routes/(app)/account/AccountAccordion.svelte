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

    let showModal = false;

</script>

<div id="user-{data.category}-accordion" class="flex flex-col w-full">
    <div id="user-{data.category}-heading" class="flex flex-row m-5 justify-start">
        <Heading tag="h4" class="">{data.title}</Heading>
        <Button on:click={() => (showModal = true)}>Add {data.title}</Button>
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

<Modal size="xs" id="{data.category}-modal" bind:open={showModal} >
    <Listgroup items={data.items} let:item>
        {item.name}
    </Listgroup>
</Modal>
