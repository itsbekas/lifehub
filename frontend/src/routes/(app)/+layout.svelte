<script lang="ts">
  import Navbar from '@/components/Navbar.svelte';
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<div class="flex min-h-screen flex-col bg-white">
  <!-- Navbar -->
  <header class="sticky top-0 z-50 bg-white shadow-sm">
    <Navbar />
  </header>

  <!-- Main Dashboard Container -->
  <main class="flex-grow px-4 py-4 md:px-6 lg:px-10">
    <div class="p-4 lg:p-6">
      {@render children?.()}
    </div>
  </main>
</div>
