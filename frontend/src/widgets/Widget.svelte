<script lang="ts">

    interface Props {
        title: string;
        href: string;
        children?: import('svelte').Snippet;
    }

    let { title, href, children }: Props = $props();
</script>

<a class="w-full" href={href}>
    <h5 class="mb-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">{title}</h5>
    {@render children?.()}
</a>