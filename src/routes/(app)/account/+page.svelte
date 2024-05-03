<script lang="ts">
    import { Accordion, AccordionItem, Button, Heading, Listgroup, Modal, TabItem } from 'flowbite-svelte';
    import UserProviderCard from './UserProviderCard.svelte';
    import UserModuleCard from './UserModuleCard.svelte';
    import AccountAccordion from './AccountAccordion.svelte';
    /** @type {import('./$types').PageData}*/
    export let data: { providers: Array<Provider>, modules: Array<Module>, user_providers: Array<Provider>, user_modules: Array<Module> };
    
    let providersData = {
        title: 'Providers',
        category: 'provider',
        cardComponent: UserProviderCard,
        user_items: data.user_providers,
        items: data.providers
    };
    let modulesData = {
        title: 'Modules',
        category: 'module',
        cardComponent: UserModuleCard,
        user_items: data.user_modules,
        items: data.modules
    };
</script>

<div class="grid grid-cols-2 grid-rows-1 gap-10">
    <AccountAccordion data={providersData} />
    <AccountAccordion data={modulesData} />
</div>
