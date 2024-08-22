<script lang="ts">

    export let title: string;
    export let href: string;
</script>

<a class="w-full" href={href}>
    <h5 class="mb-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">{title}</h5>
    <slot />
</a>