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
            // TODO: Display error in the Modal (#7)
            console.log("teste");
            return fail(response.status, { error: data.detail });
        }
        // store the token in a cookie
        cookies.set(
            'token',
            data.access_token,
            {
                path: '/',
                // maxAge: data.expires_at,
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
                sameSite: 'lax',
                secure: false //TODO: Change to secure when using HTTPS
            }
        )
        let next = formData.get('next')?.toString();

        if (next) {
            redirect(302, next);
        }
        
        return { success: true, name: data.name };
    },
}
