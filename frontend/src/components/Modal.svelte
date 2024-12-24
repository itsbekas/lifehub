<script lang="ts">
  interface Props {
    title: string;
    isOpen: boolean;
    children?: import('svelte').Snippet;
  }

  let { title, isOpen = $bindable(), children }: Props = $props();
</script>

{#if isOpen}
  <div class="fixed inset-0 flex items-center justify-center bg-black/20">
    <div class="rounded-lg bg-white p-4">
      <div class="flex justify-between gap-4">
        <h2>{title}</h2>
        <button onclick={() => (isOpen = false)}>Close</button>
      </div>
      <div class="pt-4">
        {@render children?.()}
      </div>
    </div>
  </div>
{/if}
