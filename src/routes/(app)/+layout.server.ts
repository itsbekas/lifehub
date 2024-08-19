import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export function load({ url, cookies }) {
    
    const token = cookies.get('token');
    const display_name = cookies.get('display_name');

    if (!token && url.pathname !== '/') {
        return redirect(302, '/login?next=' + url.pathname);
    }

    return {
        hasToken: !!token,
        display_name
    }

}
