<script lang="ts">
    export let navbarItems = [
        {
            title: "Dashboard",
            href: "/dashboard",
        },
        {
            title: "Settings",
            href: "/settings",
        },
    ];
</script>

<div class="py-4 px-24 align-middle border-b border-gray-300">
    <nav class="hover:font-sans flex items-center justify-between">
        <a href="/" class="text-3xl font-bold text-gray-800">Lifehub</a>
        <ul class="flex">
            {#each navbarItems as { title, href }}
                <li><a href="{ href }" class="ml-4 align-middle text-gray-600 hover:text-gray-800">{ title }</a></li>
            {/each}
        </ul>
    </nav>
</div>
