<script lang="ts">
    export let provider: Provider;
    console.log(provider);
    import { AccordionItem } from 'flowbite-svelte';
</script>

<AccordionItem>
    <p>{provider.name}</p>
</AccordionItem>
