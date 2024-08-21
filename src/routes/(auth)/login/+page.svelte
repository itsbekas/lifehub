<script>
    import TextInput from "$components/TextInput.svelte";
</script>

<form method="POST" action="/login/?/login">
    <TextInput label="Username" name="username" autocomplete="username" required />
    <TextInput label="Password" name="password" autocomplete="current-password" type="password" required />
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