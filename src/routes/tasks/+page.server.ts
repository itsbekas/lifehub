/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    let res = await fetch('http://localhost:8000/tasks/tasks');
    let data = await res.json();
    return {
        dailies: data.dailies,
        todos: data.todos,
        habits: data.habits,
    };
}
