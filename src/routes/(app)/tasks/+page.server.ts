import { fetch_api } from "$lib/api";

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    let res = await fetch_api('/tasks/tasks');
    let data = await res.json();
    return {
        dailies: data.dailies,
        todos: data.todos,
        habits: data.habits,
    };
}
