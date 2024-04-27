import { api_url } from "$lib/api";

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    let res = await fetch(api_url('/server/qbit-stats'));
    let data = await res.json();
    return {
        alltime_dl: data.alltime_dl,
        alltime_ul: data.alltime_ul,
        ratio: data.alltime_ratio,
    }
}