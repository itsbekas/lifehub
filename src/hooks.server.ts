import { redirect } from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').HandleFetch} */
export async function handleFetch({ event, request, fetch }) {

    let cookies = event.request.headers.get('cookie');

    let token = cookies && cookies.split(';')
                .find(cookie => cookie.trim().startsWith('token='))?.split('=')[1];

    if (!token && event.request.url !== '/user/login') {
        let next = new URL(event.request.url).pathname;
        // Not ideal workaround but it was redirecting the user to the page data
        if (next.endsWith('/__data.json')) {
            next = next.replace('/__data.json', '');
        }
        return redirect(302, '/user/login?next=' + next);
    }

    request.headers.set('Authorization', `Bearer ${token}`);
    return fetch(request);
}
