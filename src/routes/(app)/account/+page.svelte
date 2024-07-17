<script lang="ts">
    import AddModuleButton from './AddModuleButton.svelte';
    import UserModuleCard from './UserModuleCard.svelte';
    import AccountAccordion from './AccountAccordion.svelte';
    /** @type {import('./$types').PageData}*/
    export let data: { modules: Array<Module>, userModules: Array<Module> };

    let modulesData = {
        title: 'Modules',
        category: 'module',
        cardComponent: UserModuleCard,
        userItems: data.userModules,
        addButtonComponent: AddModuleButton,
        items: data.modules
    };
</script>

<div class="grid grid-cols-2 grid-rows-1 gap-10">
    <AccountAccordion data={modulesData} />
</div>
