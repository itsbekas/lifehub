<script lang="ts">

    import { Button, Input } from 'flowbite-svelte';

    export let data: Provider;

</script>

<div id="add-module-form-{data.name}">
    <form method="POST" action="?/addModule">
        <Input type="hidden" name="module_id" value="{data.id}" />
        <Button type="submit" size="xs">Add</Button>
    </form>
</div>
