<script lang="ts">

    import { Card } from 'flowbite-svelte';

    export let title: string;
    export let href: string;
</script>

<Card class="w-full" href={href}>
    <h5 class="mb-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">{title}</h5>
    <slot />
</Card>