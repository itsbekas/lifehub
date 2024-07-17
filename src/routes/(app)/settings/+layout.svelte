<script lang="ts">
    import SidebarNav from "$components/settings/SidebarNav.svelte";
</script>

<div class="flex flex-row">
    <div class="px-24 pt-12">
        <SidebarNav />
    </div>
    <div class="px-24 pt-12 text-sm">
        <slot />
    </div>
</div>
