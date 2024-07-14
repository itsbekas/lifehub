<script lang="ts">

    import T212Widget from "$widgets/T212Widget.svelte";
    import CalendarWidget from "$widgets/CalendarWidget.svelte";

    /** type {import('./$types').PageData} */
    export let data: { t212Data: T212Data, calendarData: Array<CalendarEvent> };

</script>

<main class="mx-10 mt-5">
    <T212Widget data={data.t212Data} />
    <CalendarWidget data={data.calendarData} />
</main>
