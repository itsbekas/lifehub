import { api_url } from '$lib/api.js';
import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export async function POST({ cookies, request }) {
    const formData = await request.formData();
    // Check if passwords match
    if (formData.get('password') !== formData.get('password-confirm')) {
        redirect(302, '/?error=Passwords do not match');
    }
    const response = await fetch(api_url('/user/signup'), {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    if (!response.ok) {
        redirect(302, `/?error=${data.detail}`);
    }
    // store the token in a cookie
    cookies.set(
        'token',
        data.access_token,
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
