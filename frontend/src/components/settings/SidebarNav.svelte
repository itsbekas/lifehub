<script lang="ts">
    let { sidebarNavItems = [
        {
            title: "Profile",
            href: "/settings/profile",
        },
        {
            title: "Providers",
            href: "/settings/providers",
        },
        {
            title: "Modules",
            href: "/settings/modules",
        },
    ] } = $props();
</script>

<div class="bg-white text-gray-900">
    <div class="flex flex-col">
        {#each sidebarNavItems as { title, href }}
            <a
                class="w-full text-left p-2 pr-24 hover:bg-gray-100 rounded-lg transition duration-200"
                href={href}
            >
                <p>{title}</p>
            </a>
        {/each}
    </div>
</div>
