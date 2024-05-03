import { api_url } from '$lib/api';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const p_response = await fetch(api_url('/providers'));
    const providers = await p_response.json();

    const m_response = await fetch(api_url('/modules'));
    const modules = await m_response.json();

    const up_response = await fetch(api_url('/user/providers'));
    const user_providers = await up_response.json();
    
    const um_response = await fetch(api_url('/user/modules'));
    const user_modules = await um_response.json();

    return { providers, modules, user_providers, user_modules };
}
