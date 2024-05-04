<script lang="ts">
    import { Accordion, AccordionItem, Button, Heading, Listgroup, Modal, TabItem } from 'flowbite-svelte';
    import UserProviderCard from './UserProviderCard.svelte';
    import UserModuleCard from './UserModuleCard.svelte';
    import AccountAccordion from './AccountAccordion.svelte';
    /** @type {import('./$types').PageData}*/
    export let data: { providers: Array<Provider>, modules: Array<Module>, userProviders: Array<Provider>, userModules: Array<Module> };
    
    let providersData = {
        title: 'Providers',
        category: 'provider',
        cardComponent: UserProviderCard,
        userItems: data.userProviders,
        items: data.providers
    };
    let modulesData = {
        title: 'Modules',
        category: 'module',
        cardComponent: UserModuleCard,
        userItems: data.userModules,
        items: data.modules
    };
</script>

<div class="grid grid-cols-2 grid-rows-1 gap-10">
    <AccountAccordion data={providersData} />
    <AccountAccordion data={modulesData} />
</div>
