import { api_url } from '$lib/api.js';
import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export async function GET({ fetch, url }) {

    const provider_id: string | null = url.searchParams.get('state');
    const code: string | null = url.searchParams.get('code');

    if (!provider_id || !code) {
        return new Response('Invalid request', { status: 400 });
    }

    const params = new URLSearchParams({ code });

    const response = await fetch(api_url(`/user/providers/${provider_id}/oauth_token?`) + params, {
        method: 'POST',
    })

    const data = await response.json();

    if (!response.ok) {
        // TODO: Improve error handling (#7)
        return redirect(301, `/account?error=${data.detail}`);
    }

    return redirect(301, '/account');

}
