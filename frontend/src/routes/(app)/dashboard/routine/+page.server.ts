import { api_url } from '$lib/api';
import type { TaskList } from '$lib/types/routine';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const tasksRequest = await fetch(api_url('/routine/tasks'));
    const tasksData: TaskList[] = await tasksRequest.json();

    return { tasksData };

}
