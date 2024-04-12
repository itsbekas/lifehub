<script>
    import { afterUpdate } from 'svelte';

    let next = '/user/account';

    afterUpdate(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const nextParam = urlParams.get('next');
        if (nextParam) {
            next = nextParam;
        }
    });

</script>

<form method="POST" action="/user/login?/login">
    <label>
        Username
        <input type="text" name="username" autocomplete="username" />
    </label>
    <label>
        Password
        <input type="password" name="password" autocomplete="current-password" />
    </label>
    <input type="hidden" name="next" value={next} />
    <button type="submit">Login</button>
</form>
