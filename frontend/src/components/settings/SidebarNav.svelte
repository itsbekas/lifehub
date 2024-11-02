<script lang="ts">
	import { Button } from "@/components/ui/button";

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

<nav class="flex flex-col">
    {#each sidebarNavItems as { title, href }}
        <Button
            variant="ghost"
            href={href}
        >
            <p class="w-full text-left text-base font-semibold text-primary">{title}</p>
        </Button>
    {/each}
</nav>
