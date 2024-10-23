import { api_url } from '$lib/api.js';
import { fail, redirect } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */
export const actions = {
    signup: async ({ request }) => {
        const formData = await request.formData();
        // Check if passwords match
        if (formData.get('password') !== formData.get('confirmPassword')) {
            redirect(302, '/?error=Passwords do not match');
        }
        const response = await fetch(api_url('/user/signup'), {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (!response.ok) {
            return fail(response.status, {error: data.detail })
        }
        
        return { success: true };
    },
}
