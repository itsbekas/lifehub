<script lang="ts">
	import type { TaskList, Event } from '@/lib/types/routine';
	import * as Card from '@/components/ui/card';
  import { Separator } from '@/components/ui/separator';
  import { Checkbox } from '@/components/ui/checkbox';
  import { Label } from '@/components/ui/label';
  import { formatDate } from '@/lib/utils';

	interface Props {
		data: { tasks: TaskList[], events: Event[] };
	}

	let { data }: Props = $props();

  function toggleTask(id: string) {
    console.log(id);
  }

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
                <div class="flex items-center">
                  <Checkbox
                    id={task.id}
                    onclick={ () => { toggleTask(task.id) }}
                  />
                  <Label for={task.id} class="ml-2 text-balance break-words">{task.title}</Label>
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
