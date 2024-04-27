import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */
export function load({ cookies }) {
    let token = cookies.get('token');
    if (!token) redirect(302, '/');

    cookies.delete('token', { path: '/' });

    redirect(302, '/');

}
