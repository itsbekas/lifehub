import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ cookies }) {
    if (!cookies.get('token')) redirect(302, '/');
}
