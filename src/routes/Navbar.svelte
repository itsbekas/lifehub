<script lang="ts">
    import { Button, Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
    import AccountIcon from '../components/AccountIcon.svelte';

    export let data: { display_name: string};

    import { loggedIn, displayName } from '$lib/stores.js';
    import { onDestroy } from 'svelte';
	import LoginSignupModal from '../components/LoginSignupModal.svelte';

    let isLoggedIn: boolean;

    const unsubscribeLoggedIn = loggedIn.subscribe(value => {
        isLoggedIn = value;
    });

    const unsubscribeDisplayName = displayName.subscribe(value => {
        data.display_name = value;
    });

    onDestroy(unsubscribeLoggedIn);
    onDestroy(unsubscribeDisplayName);

</script>

<Navbar >
    <NavBrand href={isLoggedIn ? '/dashboard' : '/'}>
        <span class="self-center whitespace-nowrap text-3xl font-semibold dark:text-white">Lifehub</span>
    </NavBrand>
    <div class="flex md:order-2">
        {#if isLoggedIn}
            <AccountIcon {data} />
        {:else}
            <LoginSignupModal />
        {/if}
        <NavHamburger />
    </div>
</Navbar>
