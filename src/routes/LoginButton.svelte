<script>
    import { Button, Modal, Checkbox, Label, Input } from 'flowbite-svelte';
    let formModal = false;
</script>

<Button size="sm" on:click={() => formModal = true}>Login</Button>

<Modal bind:open={formModal} size="xs" class="w-full" autoclose >
    <form class="flex flex-col space-y-6" method="POST" action="/login?/login">
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Sign in to Lifehub</h3>
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
            Not registered? <a href="/signup" class="text-primary-700 hover:underline dark:text-primary-500">Sign up</a>
        </div>
    </form>
</Modal>
