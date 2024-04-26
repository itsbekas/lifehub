import { redirect } from "@sveltejs/kit";

/** @type {import('./$types').Actions} */
export function load({ cookies }) {
    if (cookies.get('token')) redirect(302, '/welcome');
}
