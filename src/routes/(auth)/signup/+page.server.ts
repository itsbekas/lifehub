import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */
export function load({ cookies }) {
    if (cookies.get('token')) redirect(302, '/welcome');
}

/** @type {import('./$types').Actions} */
export const actions = {
    signup: async ({ cookies, request }) => {
        const formData = await request.formData();
        // Check if passwords match
        if (formData.get('password') !== formData.get('password-confirm')) {
            redirect(302, '/signup?error=Passwords do not match');
        }
        const response = await fetch('/user/signup', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (!response.ok) {
            redirect(302, `/signup?error=${data.detail}`);
        }
        // store the token in a cookie
        cookies.set(
            'token',
            data.token,
            {
                path: '/',
                // expires: data.expires_at,
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
        redirect(302, '/account')
    }
}
