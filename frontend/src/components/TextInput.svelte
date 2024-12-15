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
  {type}
  {name}
  id={name}
  {placeholder}
  class="w-full rounded-lg border border-gray-300 text-sm"
  {autocomplete}
  {required}
/>
