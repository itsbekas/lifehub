<script lang="ts">
    interface Props {
        title: string;
        description?: string;
        placeholder?: string;
        value?: string;
        name?: string;
        type?: "text" | "password";
        autocomplete?: string;
    }

    let {
        title,
        description = "",
        placeholder = "",
        value = "",
        name = "",
        type = "text",
        autocomplete = "off"
    }: Props = $props();
</script>

<div class="flex flex-col mb-4">
    <label>
        <p class="font-semibold">{ title }</p>
        {#if description}
            <p class="text-xs text-gray-500 mb-1">{ description }</p>
        {/if}
        <input
            type={ type } name={ name }
            placeholder={ placeholder } value={ value }
            autocomplete={ autocomplete }
            class="rounded-lg text-sm border border-gray-300 p-2 w-2/3
            hover:border-gray-400
            focus:border-gray-800"
        >
    </label>
</div>