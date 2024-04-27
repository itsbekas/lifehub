<script lang="ts">
    import ProviderCard from './ProviderCard.svelte';
    /** @type {import('./$types').PageData}*/
    export let data: { providers: Array<Provider> };
</script>

<main>
    <h1>Providers</h1>
    {#each data.providers as provider}
        <ProviderCard {provider} />
    {/each}
</main>
