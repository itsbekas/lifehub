import { api_url } from '$lib/api';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const userResponse = await fetch(api_url('/user/me'));
    const user = await userResponse.json();

    return { user };
}
