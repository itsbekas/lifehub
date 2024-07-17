import { api_url } from '$lib/api';
import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const mResponse = await fetch(api_url('/modules'));
    const modules = await mResponse.json();
    
    const um_response = await fetch(api_url('/user/modules'));
    const userModules = await um_response.json();

    return { modules, userModules };
}

/** @type {import('./$types').Actions} */
export const actions = {

    addModule: async ({ fetch, request }) => {
        const formData = await request.formData();

        const response = await fetch(api_url(`/user/modules/${formData.get('module_id')}`), {
            method: 'POST',
        })
        const data = await response.json();
        if (!response.ok) {
            // TODO: Improve error handling (#7)
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
            // TODO: Improve error handling (#7)
            return { error: data.detail };
        }
    }
}
