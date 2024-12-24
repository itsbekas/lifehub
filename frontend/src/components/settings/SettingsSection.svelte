<script lang="ts">
  interface Props {
    title: string;
    description: string;
    children?: import('svelte').Snippet;
  }

  let { title, description, children }: Props = $props();
</script>

<div id="{title}-provider-settings-section" class="mb-4 w-full border-b pb-2">
  <h2 class="text-lg font-bold text-gray-800">{title}</h2>
  <p class="text-sm text-gray-600">{description}</p>
</div>
<div class="mb-8">
  {@render children?.()}
</div>
