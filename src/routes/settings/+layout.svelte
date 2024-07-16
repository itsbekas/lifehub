<script lang="ts">
    import Navbar from '$components/Navbar.svelte';
    import SidebarNav from "$components/settings/SidebarNav.svelte";
</script>

<Navbar />
<div class="flex flex-row">
    <div class="px-24 pt-12">
        <SidebarNav />
    </div>
    <div class="px-24 pt-12 text-sm">
        <slot />
    </div>
</div>
