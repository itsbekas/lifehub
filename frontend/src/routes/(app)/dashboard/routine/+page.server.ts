import { api_url } from '$lib/api';
import type { TaskList, Event } from '$lib/types/routine';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
  const [tasksRequest, eventsRequest] = await Promise.all([
    fetch(api_url('/routine/tasks')),
    fetch(api_url('/routine/events'))
  ]);

  const tasksData: TaskList[] = await tasksRequest.json();
  const eventsData: Event[] = await eventsRequest.json();

  return { tasks: tasksData, events: eventsData };
}

/** @satisfies {import('./$types').Actions} */
export const actions = {
  deleteTask: async ({ fetch, request }) => {
    const formData = await request.formData();
    const response = await fetch(
      api_url(`/routine/tasks/${formData.get('tasklist_id')}/${formData.get('task_id')}`),
      { method: 'DELETE' }
    );
    const data = await response.json();
    return data;
  },

  toggleTask: async ({ fetch, request }) => {
    const formData = await request.formData();
    const response = await fetch(
      api_url(`/routine/tasks/${formData.get('tasklist_id')}/${formData.get('task_id')}/toggle`),
      {
        method: 'PATCH'
      }
    );
    const data = await response.json();
    return data;
  }
};
