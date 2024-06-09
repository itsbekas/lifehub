<script lang="ts">
    import { Accordion, AccordionItem, Button, Heading, Listgroup } from 'flowbite-svelte';

    /** type {import('./$types').PageData} */
    export let data: { t212Data: t212Data };
</script>

<div class="grid grid-cols-2 grid-rows-1 gap-10">
    <div>
        <Heading size="md">Balance</Heading>
        <p>Available: {data.t212Data.balance.free}</p>
        <p>Invested: {data.t212Data.balance.invested}</p>
        <p>Result: {data.t212Data.balance.result}</p>
    </div>
    <div>
        <Heading size="md">History</Heading>
        <Listgroup>
            {#each data.t212Data.history as item}
            <div class="flex flex-row justify-between align-middle h-full">
                <p>{item.timestamp}</p>
                <p>{item.amount.toFixed(2)}</p>
                <p>{item.type}</p>
            </div>
            {/each}
        </Listgroup>
    </div>
</div>