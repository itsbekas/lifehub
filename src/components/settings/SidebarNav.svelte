<script lang="ts">
    import '../../app.pcss';
    import { Button } from "bits-ui";

    export let sidebarNavItems = [
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
    ];
</script>

<div class="bg-white text-gray-900 min-h-screen pl-24 pt-2">
    <div class="flex flex-col">
        {#each sidebarNavItems as { title, href }}
            <Button.Root
                class="w-full text-left p-2 hover:bg-gray-100 rounded-lg transition duration-200"
                href={href}
            >
                <p>{title}</p>
            </Button.Root>
        {/each}
    </div>
</div>
