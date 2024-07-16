<script lang="ts">
    import ProviderCard from '$components/settings/ProviderCard.svelte';
    import SectionTitle from '$components/settings/SectionTitle.svelte';

    /** @type {import('./$types').PageData}*/
    export let data: { providers: Array<Provider>, userProviders: Array<Provider> };
</script>

<SectionTitle title="Providers" />
<div class="mt-2">
    {#each data.providers as provider}
        <div class="mb-2">
            <ProviderCard provider={provider}/>
        </div>
    {/each}
</div>
