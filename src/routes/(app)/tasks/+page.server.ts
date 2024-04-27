import { api_url } from "$lib/api";

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    let res = await fetch(api_url('/tasks/tasks'));
    let data = await res.json();
    return {
        dailies: data.dailies,
        todos: data.todos,
        habits: data.habits,
    };
}
