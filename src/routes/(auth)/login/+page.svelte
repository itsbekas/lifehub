<script>
    import TextInput from "$components/TextInput.svelte";
</script>

<form method="POST" action="/login/?/login">
    <label>
        <span>Username</span>
        <TextInput name="username" autocomplete="username" required />
    </label>
    <label>
        <span>Password</span>
        <TextInput name="password" autocomplete="current-password" type="password" required />
    </label>
    <div>
        <input type="checkbox" name="remember">
        <span>Remember me</span>
    </div>
    <button type="submit">Login</button>
    <div>
        Not registered?
        <a href="/signup">Sign up</a>
    </div>
</form>