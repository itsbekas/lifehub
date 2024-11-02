<script lang="ts">
    import Navbar from '@/components/Navbar.svelte';
    interface Props {
        children?: import('svelte').Snippet;
    }

    let { children }: Props = $props();
</script>

<Navbar />
{@render children?.()}
