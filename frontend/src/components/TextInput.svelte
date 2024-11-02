<!-- Basic text input -->
<script lang="ts">
    interface Props {
        label: string;
        placeholder?: string;
        name: string;
        required?: boolean;
        autocomplete?: string;
        type?: string;
    }

    let {
        label,
        placeholder = '',
        name,
        required = false,
        autocomplete = 'off',
        type = 'text'
    }: Props = $props();
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
