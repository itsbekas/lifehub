import { api_url } from '$lib/api';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    const p_response = await fetch(api_url('/user/providers'));
    const providers = await p_response.json();
    
    const m_response = await fetch(api_url('/user/modules'));
    const modules = await m_response.json();

    return { providers, modules };
}
