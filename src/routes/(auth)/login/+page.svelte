<script>
    import { afterUpdate } from 'svelte';
    import { Input, Label, A, Button } from 'flowbite-svelte';

    let next = '/account';

    afterUpdate(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const nextParam = urlParams.get('next');
        if (nextParam) {
            next = nextParam;
        }
    });

</script>

<body class="flex justify-center items-center h-screen m-0">
    <div class="flex flex-col justify-between items-center">
        <form method="POST" action="/login?/login">
            <Label class="mb-2">
                <span>Username</span>
                <Input type="text" name="username" autocomplete="username" required />
            </Label>
            <Label class="mb-2">
                <span>Password</span>
                <Input type="password" name="password" autocomplete="current-password" required />
            </Label>
            <input type="hidden" name="next" value={next} />
            <Button type="submit">Login</Button>
        </form>

        <p>Want to <A href="/signup?next={next}">register</A>?</p>
    </div>
</body>

<style>

    form {
        display: flex;
        flex-direction: column;
    }

</style>
