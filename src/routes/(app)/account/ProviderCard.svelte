<script lang="ts">
    export let provider: Provider;
    console.log(provider);
    import { AccordionItem } from 'flowbite-svelte';
</script>

<AccordionItem>
    <span slot="header">{provider.name}</span>
    <p>{provider.name}</p>
</AccordionItem>
