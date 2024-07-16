<script lang="ts">
    import Navbar from '$components/Navbar.svelte';
    import SidebarNav from "$components/settings/SidebarNav.svelte";
</script>

<Navbar />
<div class="flex flex-row">
    <div class="px-24 pt-8">
        <SidebarNav />
    </div>
    <div class="pt-8 text-sm">
        <slot />
    </div>
</div>
