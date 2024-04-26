<body>
    <div class="signup">
        <form method="POST" action="/signup?/signup">
            <label>
                Name
                <input type="text" name="name" autocomplete="name" />
            </label>
            <label>
                Username
                <input type="text" name="username" autocomplete="username" />
            </label>
            <label>
                Password
                <input type="password" name="password" autocomplete="new-password" />
            </label>
            <label>
                Confirm password
                <input type="password" name="password-confirm" autocomplete="new-password" />
            </label>
            <button type="submit">Sign up</button>
        </form>
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

    div.signup {
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