<script lang="ts">
    import { Button, Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
    import LoginButton from './LoginButton.svelte';
    import AccountIcon from './AccountIcon.svelte';

    export let data: { loggedIn: boolean, display_name: string};

</script>

<Navbar >
    <NavBrand href="/">
        <span class="self-center whitespace-nowrap text-3xl font-semibold dark:text-white">Lifehub</span>
    </NavBrand>
    <div class="flex md:order-2">
        {#if data.loggedIn}
            <AccountIcon {data} />
        {:else}
            <LoginButton />
        {/if}
        <NavHamburger />
    </div>
</Navbar>
