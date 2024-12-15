<script lang="ts">
  import SidebarNav from '@/components/settings/SidebarNav.svelte';
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<div class="flex flex-row justify-center">
  <div class="pt-12">
    <SidebarNav />
  </div>
  <div class="w-1/3 px-24 pt-12 text-sm">
    {@render children?.()}
  </div>
</div>
