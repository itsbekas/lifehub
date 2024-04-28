<script lang="ts">
    import { A, Avatar, Button, Dropdown, DropdownItem } from 'flowbite-svelte';

    export let data: { loggedIn: boolean, display_name: string };
</script>

<Dropdown triggeredBy="#account-icon">
    <DropdownItem>
        <A href="/account">Account</A>
    </DropdownItem>
    <DropdownItem slot="footer">
        <A href="/logout">Sign out</A>
    </DropdownItem>
</Dropdown>

<Button id="account-icon" size="sm" color="light" class="text-gray-900 dark:text-white">
    <Avatar size="xs" />
    <span class="ml-2">
        {data.display_name}
    </span>
</Button>
