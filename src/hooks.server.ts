import { redirect } from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').HandleFetch} */
export async function handleFetch({ event, request, fetch }) {

    let cookies = event.request.headers.get('cookie');

    let token = cookies && cookies.split(';')
                .find(cookie => cookie.trim().startsWith('token='))?.split('=')[1];

    if (!token && event.request.url !== '/login') {
        let next = new URL(event.request.url).pathname;
        return redirect(302, '/login?next=' + next);
    }

    request.headers.set('Authorization', `Bearer ${token}`);
    return fetch(request);
}
