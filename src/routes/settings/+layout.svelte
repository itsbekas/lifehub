<script lang="ts">
    import Navbar from '$components/Navbar.svelte';
    import SidebarNav from "$components/settings/SidebarNav.svelte";
</script>

<Navbar />
<div class="flex flex-row">
    <div class="px-24 py-8">
        <SidebarNav />
    </div>
    <div class="py-8">
        <slot />
    </div>
</div>
