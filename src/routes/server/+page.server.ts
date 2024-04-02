/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    let res = await fetch('http://localhost:8000/server/qbit-stats');
    let data = await res.json();
    return {
        alltime_dl: data.dl,
        alltime_ul: data.ul,
        ratio: data.ratio,
    }
}