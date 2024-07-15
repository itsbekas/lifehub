<script lang="ts">
    import Card from '$components/settings/Card.svelte';
    import SectionTitle from '$components/settings/SectionTitle.svelte';

    /** @type {import('./$types').PageData}*/
    export let data: { providers: Array<Provider>, userProviders: Array<Provider> };
</script>

<SectionTitle title="Providers" />
{#each data.providers as provider}
    <Card />
{/each}
