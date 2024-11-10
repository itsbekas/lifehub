<script lang="ts">
  import type { TaskList, Event } from '@/lib/types/routine';
  import * as Card from '@/components/ui/card';
  import { Separator } from '@/components/ui/separator';
  import { Button } from '@/components/ui/button';
  import { formatDate } from '@/lib/utils';
  import CircleCheckBig from 'lucide-svelte/icons/circle-check-big';
  import Trash2 from 'lucide-svelte/icons/trash-2';

  interface Props {
    data: { tasks: TaskList[], events: Event[] };
  }

  let { data }: Props = $props();

</script>

<main class="mx-5 mt-5">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
  <div>
    <h1 class="text-3xl font-bold text-primary">Tasks</h1>
    <Card.Root class="mb-5">
    {#each data.tasks as taskList}
      <Card.Content>
        <Card.Title>
          {taskList.title}
        </Card.Title>
        <Separator class="my-2"/>
        <div class="flex flex-col space-y-2">
          {#each taskList.tasks as task}
            <div class="flex items-center gap-2 hover:bg-accent p-2 rounded">
              <p class="w-full text-balance break-words">{task.title}</p>
              <form method="post" action="?/toggleTask">
                <input type="hidden" name="tasklist_id" value={taskList.id} />
                <input type="hidden" name="task_id" value={task.id} />
                <Button
                  variant="outline"
                  size="icon"
                  class="hover:bg-green-500 hover:text-white"
                  type="submit"
                >
                  <CircleCheckBig class="w-6 h-6 text-balance"/>
                </Button>
              </form>
              <form method="post" action="?/deleteTask">
                <input type="hidden" name="tasklist_id" value={taskList.id} />
                <input type="hidden" name="task_id" value={task.id} />
                <Button
                  variant="outline"
                  size="icon"
                  class="hover:bg-red-500 hover:text-white"
                  type="submit"
                >
                  <Trash2 class="w-6 h-6"/>
                </Button>
              </form>
            </div>
          {/each}
        </div>
      </Card.Content>
    {/each}
    </Card.Root>
  </div>
  <div>
    <h1 class="text-3xl font-bold text-primary">Events</h1>
    <Card.Root class="mb-5">
    {#each data.events as event}
      <Card.Content>
      <Card.Title>
        {event.title}
      </Card.Title>
      <div class="text-sm">
        <p>Start: {formatDate(event.start)}</p>
        <p>End: {formatDate(event.end)}</p>
        {#if event.location}
        <p>Location: {event.location}</p>
        {/if}
      </div>
      </Card.Content>
    {/each}
    </Card.Root>
  </div>
  </div>
</main>
