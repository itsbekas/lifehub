<script lang="ts">
    import { Accordion, AccordionItem, Heading } from 'flowbite-svelte';
    import ProviderCard from './ProviderCard.svelte';
    import ModuleCard from './ModuleCard.svelte';
    /** @type {import('./$types').PageData}*/
    export let data: { providers: Array<Provider>, modules: Array<Module> };
</script>

<main>
    <div class="flex justify-center">
        <div id="user-providers" class="flex flex-col w-1/4 m-8">
            <Heading tag="h3" class="mb-4">Providers</Heading>
            <Accordion>
                {#each data.providers as provider}
                <AccordionItem>
                    <span slot="header">{provider.name} (ID: {provider.id})</span>
                    <ProviderCard {provider} />
                </AccordionItem>
                {/each}
            </Accordion>
        </div>
        <div id="user-modules" class="flex flex-col w-1/4 m-8">
            <Heading tag="h3" class="mb-4">Modules</Heading>
            <Accordion>
                {#each data.modules as module}
                <AccordionItem>
                    <span slot="header">{module.name} (ID: {module.id})</span>
                    <ModuleCard {module} />
                </AccordionItem>
                {/each}
            </Accordion>
        </div>
    </div>
</main>
