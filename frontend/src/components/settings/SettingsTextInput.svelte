<script lang="ts">
    export let title: string;
    export let description: string = "";
    export let placeholder: string = "";
    export let value: string = "";
    export let name: string = "";
    export let type: "text" | "password" = "text";
    export let autocomplete: string = "off";
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