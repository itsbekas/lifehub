<script lang="ts">
    import '../app.pcss';
    interface Props {
        children?: import('svelte').Snippet;
    }

    let { children }: Props = $props();
</script>

<main>
    {@render children?.()}
</main>
