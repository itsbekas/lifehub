import { api_url } from '$lib/api';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    const response = await fetch(api_url('/user/providers'));
    const providers = await response.json();
    return { providers };
}
