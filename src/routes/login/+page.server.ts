import { fetch_api } from '$lib/api';
import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */
export function load({ cookies }) {
    if (cookies.get('token')) redirect(302, '/account');
}

/** @type {import('./$types').Actions} */
export const actions = {
    login: async ({ cookies, request }) => {
        const formData = await request.formData();
        const response = await fetch_api('/user/login', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (!response.ok) {
            redirect(302, `/login?error=${data.detail}`);
        }
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
