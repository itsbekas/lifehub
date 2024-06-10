import { api_url } from '$lib/api';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const t212Request = await fetch(api_url('/finance/trading212/data'));
    const t212Data = await t212Request.json();

    return { t212Data };

}
