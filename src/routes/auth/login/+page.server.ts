import { api_url } from '$lib/api';
import { fail, redirect } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */
export const actions = {
    login: async ({ request, cookies }) => {
        const formData = await request.formData();
        const response = await fetch(api_url('/user/login'), {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: data.detail });
        }
        
        let expires;
        if (formData.get('remember') === 'on') {
            expires = new Date(data.expires_at);
        }

        // store the token in a cookie
        cookies.set(
            'token',
            data.access_token,
            {
                path: '/',
                expires,
                httpOnly: true,
                sameSite: 'lax',
                secure: false //TODO: Change to secure when using HTTPS
            }
        );
        cookies.set(
            'display_name',
            data.name,
            {
                path: '/',
                expires,
                sameSite: 'lax',
                secure: false //TODO: Change to secure when using HTTPS
            }
        )
        const next = formData.get('next')?.toString();

        if (next) {
            redirect(302, next);
        }
        
        return { success: true, name: data.name };
    },
}
