<!-- Basic text input -->
<script lang="ts">
    export let label: string;
    export let placeholder: string = '';
    export let name: string;
    export let required: boolean = false;
    export let autocomplete: string = 'off';
    export let type: string = 'text';
</script>

{#if label}
    <label for={name}>{label}</label>
{/if}
<input
    type={type}
    name={name}
    id={name}
    placeholder={placeholder}
    class="border border-gray-300 rounded-lg w-full text-sm"
    autocomplete={autocomplete}
    required={required}
/>
