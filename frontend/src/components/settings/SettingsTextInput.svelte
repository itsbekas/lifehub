<script lang="ts">
    import { Label } from "@/components/ui/label";
    import { Input } from "@/components/ui/input";
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

<div class="flex flex-col mb-4 gap-1">
    <Label for={ name }>{ title }</Label>
    {#if description}
        <p class="text-xs text-muted-foreground">{ description }</p>
    {/if}
    <Input
        type={ type } name={ name }
        placeholder={ placeholder } value={ value }
        autocomplete={ autocomplete }
        class="rounded-lg text-sm border border-gray-300 p-2 w-2/3
        hover:border-gray-400
        focus:border-gray-800"
    />
</div>