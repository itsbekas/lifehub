<script lang="ts">
    import Widget from '$widgets/Widget.svelte';

    interface Props {
        data: Array<CalendarEvent>;
    }

    let { data }: Props = $props();

</script>

<Widget title="Calendar" href="/modules/calendar/">
    <div class="flex flex-col space-y-2">
        {#each data as event}
            <div class="flex flex-col space-y-1">
                <span>{event.title}: {event.start}</span>
            </div>
        {/each}
    </div>
</Widget>
