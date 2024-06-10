import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ cookies }) {
    const token = cookies.get('token');
    if (!token) {
        return redirect(302, '/?login');
    }
}
