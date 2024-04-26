<script>
	import { bytes_to_human_readable } from '$lib/conversions';

    /** @type {import('./$types').PageData}*/
    export let data;

</script>

<main>
    <h1>All-Time Download: {bytes_to_human_readable(data.alltime_dl)}</h1>
    <h1>All-Time Upload: {bytes_to_human_readable(data.alltime_ul)}</h1>
    <h1>Ratio: {data.ratio}</h1>
</main>
