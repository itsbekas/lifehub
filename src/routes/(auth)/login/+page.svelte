<script>
    import { afterUpdate } from 'svelte';

    let next = '/account';

    afterUpdate(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const nextParam = urlParams.get('next');
        if (nextParam) {
            next = nextParam;
        }
    });

</script>

<body>
    <div class="login">
        <form method="POST" action="/login?/login">
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

        <p>Want to <a href="/signup?next={next}">register</a>?</p>
    </div>
</body>

<style>
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    div.login {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }

    form {
        display: flex;
        flex-direction: column;
    }

    label {
        display: flex;
        flex-direction: column;
        margin: 0.5rem;
    }

    button {
        flex: 0;
        margin: 0.5rem;
    }

</style>