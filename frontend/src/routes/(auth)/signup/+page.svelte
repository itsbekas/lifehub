<script>
    import TextInput from "@/components/TextInput.svelte";
</script>

<form method="POST" action="/signup/?/signup">
    <label for="email">
        <span>Email</span>
        <TextInput name="email" autocomplete="email" type="email" required />
    </label>
    <label for="username">
        <span>Username</span>
        <TextInput name="username" autocomplete="username" required />
    </label>
    <label for="name">
        <span>Display Name</span>
        <TextInput name="name" autocomplete="name" required />
    </label>
    <label for="password">
        <span>Password</span>
        <TextInput name="password" autocomplete="new-password" type="password" required />
    </label>
    <label for="confirmPassword">
        <span>Confirm Password</span>
        <TextInput name="confirmPassword" autocomplete="new-password" type="password" required />
    </label>
    <button type="submit">Sign Up</button>
    <div>
        Already registered?
        <a href="/login">Login</a>
    </div>
</form>
