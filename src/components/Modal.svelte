<script lang="ts">

    export let title: string;
    export let isOpen: boolean;
</script>

{#if isOpen}
    <div class="fixed inset-0 bg-black/20 flex items-center justify-center">
        <div class="bg-white p-4 rounded-lg">
            <div class="flex gap-4 justify-between">
                <h2>{ title }</h2>
                <button on:click={() => isOpen = false}>Close</button>
            </div>
            <slot />
        </div>
    </div>
{/if}
