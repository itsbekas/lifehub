<script lang="ts">
    import { Accordion, AccordionItem, Button, Heading, Listgroup, Modal, TabItem } from 'flowbite-svelte';
    import UserProviderCard from './UserProviderCard.svelte';
    import UserModuleCard from './UserModuleCard.svelte';
    /** @type {import('./$types').PageData}*/
    export let data: { providers: Array<Provider>, modules: Array<Module>, user_providers: Array<Provider>, user_modules: Array<Module> };

    let providersModal = false;
    let modulesModal = false;

</script>

<div class="grid grid-cols-2 grid-rows-1 gap-10">
    <div id="user-providers" class="flex flex-col w-full">
        <div id="user-providers-heading" class="flex flex-row m-5 justify-start">
            <Heading tag="h4" class="">Providers</Heading>
            <Button on:click={() => (providersModal = true)}>Add Provider</Button>
        </div>
        <Accordion>
            {#each data.user_providers as provider}
            <AccordionItem>
                <span slot="header">{provider.name} (ID: {provider.id})</span>
                <UserProviderCard {provider} />
            </AccordionItem>
            {/each}
        </Accordion>
    </div>
    <div id="user-modules" class="flex flex-col w-full">
        <div id="user-modules-heading" class="flex flex-row m-5">
            <Heading tag="h4" class="">Modules</Heading>
            <Button on:click={() => (modulesModal = true)}>Add Module</Button>
        </div>
        <Accordion>
            {#each data.user_modules as module}
            <AccordionItem>
                <span slot="header">{module.name} (ID: {module.id})</span>
                <UserModuleCard {module} />
            </AccordionItem>
            {/each}
        </Accordion>
    </div>
</div>

<Modal size="xs" id="providers-modal" bind:open={providersModal} >
    <Listgroup items={data.providers.map(provider => provider.name)} let:item>
        {item}
    </Listgroup>
</Modal>

<Modal id="modules-modal" bind:open={modulesModal} >
    <Listgroup items={data.modules.map(module => module.name)} let:item>
        {item}
    </Listgroup>
</Modal>
