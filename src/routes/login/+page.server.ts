import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */
export const actions = {
    login: async ({ cookies, request }) => {
        const formData = await request.formData();
        const response = await fetch('http://localhost:8000/auth/token', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        // store the token in a cookie
        cookies.set(
            'token',
            data.access_token,
            {
                path: '/',
                maxAge: data.expires_in,
                httpOnly: true,
                sameSite: 'lax',
                secure: false //TODO: Change to secure when using HTTPS
            }
        );
        let next = formData.get('next')?.toString() || '/';
        redirect(302, next);
    }
}