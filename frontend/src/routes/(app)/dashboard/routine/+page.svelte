<script lang="ts">
	import type { TaskList } from '@/lib/types/routine';
	import * as Card from '@/components/ui/card';
  import { Separator } from '@/components/ui/separator';
  import { Checkbox } from '@/components/ui/checkbox';
  import { Label } from '@/components/ui/label';

	interface Props {
		data: { tasksData: TaskList[] };
	}

	let { data }: Props = $props();

  function toggleTask(id: string) {
    console.log(id);
  }

</script>
<main class="mx-10 mt-5">
  <Card.Root class="mb-5">
    {#each data.tasksData as taskList}
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
              <Label for={task.id} class="ml-2">{task.title}</Label>
            </div>
          {/each}
        </div>
      </Card.Content>
    {/each}
  </Card.Root>
</main>

<!-- onClick: () => { completeTask(id) } -->