import { fetch_api } from "$lib/api";

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    let res = await fetch_api('/finance/networth');
    let data = await res.json();
    return {
        cash: data.bank_cash,
        uninvested: data.uninvested_cash,
        invested: data.invested,
        returns: data.returns,
        total: data.total,
    };
}
