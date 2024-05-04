import { api_url } from '$lib/api';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const pResponse = await fetch(api_url('/providers'));
    const providers = await pResponse.json();

    const mResponse = await fetch(api_url('/modules'));
    const modules = await mResponse.json();

    const upResponse = await fetch(api_url('/user/providers'));
    const userProviders = await upResponse.json();
    
    const um_response = await fetch(api_url('/user/modules'));
    const userModules = await um_response.json();

    return { providers, modules, userProviders, userModules };
}

/** @type {import('./$types').Actions} */
export const actions = {
    deleteProvider: async ({ fetch, request }) => {
        const formData = await request.formData();

        const response = await fetch(api_url(`/user/providers/${formData.get('provider_id')}`), {
            method: 'DELETE',
        })
        const data = await response.json();
        if (!response.ok) {
            // TODO: Improve error handling
            return { error: data.detail };
        }
    },

    deleteModule: async ({ fetch, request }) => {
        const formData = await request.formData();

        const response = await fetch(api_url(`/user/modules/${formData.get('module_id')}`), {
            method: 'DELETE',
        })
        const data = await response.json();
        if (!response.ok) {
            // TODO: Improve error handling
            return { error: data.detail };
        }
    }
}