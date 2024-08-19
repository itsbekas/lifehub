<form method="POST" action="/login/?/login">
    <label>
        <span>Username</span>
        <input type="text" name="username" autocomplete="username" required>
    </label>
    <label>
        <span>Password</span>
        <input type="password" name="password" autocomplete="current-password" required>
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