<script lang="ts">
    import Navbar from '@/components/Navbar.svelte';
    interface Props {
        children?: import('svelte').Snippet;
    }

    let { children }: Props = $props();
</script>

<div class="min-h-screen bg-white flex flex-col">
    <!-- Navbar -->
    <header class="shadow-sm bg-white sticky top-0 z-50">
        <Navbar />
    </header>
  
    <!-- Main Dashboard Container -->
    <main class="flex-grow px-4 md:px-6 lg:px-10 py-4">
        <div class="p-4 lg:p-6">
            {@render children?.()}
        </div>
    </main>
</div>
