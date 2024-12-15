<script lang="ts">
  import T212Widget from '@/widgets/T212Widget.svelte';

  interface Props {
    /** type {import('./$types').PageData} */
    data: { t212Data: T212Data };
  }

  let { data }: Props = $props();
</script>

<main class="mx-10 mt-5">
  <T212Widget data={data.t212Data} />
</main>
