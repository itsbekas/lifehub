<script lang="ts">
    import Navbar from '$components/Navbar.svelte';
    import SidebarNav from "$components/settings/SidebarNav.svelte";
</script>

<Navbar />
<div class="flex flex-row">
    <div class="w-60 pl-24 pr-12 py-8">
        <SidebarNav />
    </div>
    <div class="py-8">
        <slot />
    </div>
</div>
