<script lang="ts">
    import { applyAction, enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
    import { displayName, loggedIn } from '$lib/stores.js';
    import { A, Button, Checkbox, Modal, Label, Input } from 'flowbite-svelte';

    let showLoginModal = false;
    let showSignupModal = false;

    let LOGIN = 0;
    let SIGNUP = 1;

    function showModal(modal: number) {
        if (modal == LOGIN) {
            showLoginModal = true;
            showSignupModal = false;
        } else if (modal == SIGNUP) {
            showLoginModal = false;
            showSignupModal = true;
        }
    }
    
    let error: string | null = null;

</script>

<Button size="sm" on:click={() => showLoginModal = true}>Login</Button>

<Modal bind:open={showLoginModal} size="xs" class="w-full" autoclose={false} >
    <form class="flex flex-col space-y-6" method="POST" action="/auth/login/?/login"
        use:enhance={({ }) => {

            return async ({ result }) => {
                console.log(result);
                if (result.type === 'failure') {
                    error = result.data?.error;
                } else if (result.type === 'success') {
                    loggedIn.set(true);
                    displayName.set(result.data?.name);
                }
            };
        }}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Sign in to Lifehub</h3>
        {#if error}
            <div class="p-2 text-red-500 bg-red-100 rounded">
                {error}
            </div>
        {/if}
        <Label class="space-y-2">
            <span>Username</span>
            <Input type="text" name="username" autocomplete="username" required />
        </Label>
        <Label class="space-y-2">
            <span>Password</span>
            <Input type="password" name="password" autocomplete="current-password" required />
        </Label>
        <div class="flex items-start">
            <Checkbox>Remember me</Checkbox>
        </div>
        <Button type="submit" class="w-full1">Login</Button>
        <div class="text-sm font-medium text-gray-500 dark:text-gray-300">
            Not registered?
            <A on:click={() => showModal(SIGNUP)}>Sign up</A>   
        </div>
    </form>
</Modal>

<Modal bind:open={showSignupModal} size="xs" class="w-full" autoclose={false} >
    <form class="flex flex-col space-y-6" method="POST" action="/auth/signup?/signup">
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Sign up to Lifehub</h3>
        <Label class="space-y-2">
            <span>Username</span>
            <Input type="text" name="username" autocomplete="username" required />
        </Label>
        <Label class="space-y-2">
            <span>Display Name</span>
            <Input type="text" name="name" autocomplete="name" required />
        </Label>
        <Label class="space-y-2">
            <span>Password</span>
            <Input type="password" name="password" autocomplete="new-password" required />
        </Label>
        <Label class="space-y-2">
            <span>Confirm password</span>
            <Input type="password" name="password-confirm" autocomplete="new-password" required />
        </Label>
        <Button type="submit" class="w-full1">Sign up</Button>
        <div class="text-sm font-medium text-gray-500 dark:text-gray-300">
            Already registered?
            <A on:click={() => showModal(LOGIN)}>Login</A>
        </div>
    </form>
</Modal>
