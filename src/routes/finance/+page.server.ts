/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    let res = await fetch('http://localhost:8000/finance/networth');
    let data = await res.json();
    return {
        total: data.total,
    };
}
