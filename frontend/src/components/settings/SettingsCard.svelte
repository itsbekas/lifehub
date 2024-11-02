<script lang="ts">
    interface Props {
        children?: import('svelte').Snippet;
    }

    let { children }: Props = $props();

</script>

<div class="bg-white border border-gray-300 rounded-lg p-2 hover:bg-gray-100">
    {@render children?.()}
</div>
