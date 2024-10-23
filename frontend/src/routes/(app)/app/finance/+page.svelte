<script lang="ts">
    import InvestmentChart from "$components/app/finance/InvestmentChart.svelte";

    /** type {import('./$types').PageData} */
    export let data: { t212Data: T212Data };
</script>

<main class="mx-10 mt-5">
    <InvestmentChart data={data.t212Data} />
</main>
