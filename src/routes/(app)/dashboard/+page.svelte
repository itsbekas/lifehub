<script lang="ts">

    import T212Widget from "$widgets/T212Widget.svelte";

    /** type {import('./$types').PageData} */
    export let data: { t212Data: t212Data };

</script>

<main class="mx-10 mt-5">
    <T212Widget data={data.t212Data} />
</main>
