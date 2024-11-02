<script lang="ts">

    interface Props {
        title: string;
        isOpen: boolean;
        children?: import('svelte').Snippet;
    }

    let { title, isOpen = $bindable(), children }: Props = $props();
</script>

{#if isOpen}
    <div class="fixed inset-0 bg-black/20 flex items-center justify-center">
        <div class="bg-white p-4 rounded-lg">
            <div class="flex gap-4 justify-between">
                <h2>{ title }</h2>
                <button onclick={() => isOpen = false}>Close</button>
            </div>
            <div class="pt-4">
                {@render children?.()}
            </div>
        </div>
    </div>
{/if}
