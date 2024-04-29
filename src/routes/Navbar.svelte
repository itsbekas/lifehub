<script lang="ts">
    import { Button, Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
    import LoginButton from './LoginButton.svelte';
    import AccountIcon from './AccountIcon.svelte';

    export let data: { display_name: string};

    import { loggedIn } from '$lib/stores.js';
    import { onDestroy } from 'svelte';

    let isLoggedIn: boolean;

    const unsubscribe = loggedIn.subscribe(value => {
        isLoggedIn = value;
    });

    onDestroy(unsubscribe);

</script>

<Navbar >
    <NavBrand href="/">
        <span class="self-center whitespace-nowrap text-3xl font-semibold dark:text-white">Lifehub</span>
    </NavBrand>
    <div class="flex md:order-2">
        {#if isLoggedIn}
            <AccountIcon {data} />
        {:else}
            <LoginButton />
        {/if}
        <NavHamburger />
    </div>
</Navbar>
