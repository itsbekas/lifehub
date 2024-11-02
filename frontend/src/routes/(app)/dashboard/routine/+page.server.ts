import { api_url } from '$lib/api';
import type { TaskList, Event } from '$lib/types/routine';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {

    const tasksRequest = await fetch(api_url('/routine/tasks'));
    const tasksData: TaskList[] = await tasksRequest.json();

    const eventsRequest = await fetch(api_url('/calendar/events'));
    const eventsData: Event[] = await eventsRequest.json();

    return { tasks: tasksData, events: eventsData };

}
