<script lang="ts">
    import InvestmentChart from "@/components/app/finance/InvestmentChart.svelte";

    
    interface Props {
        /** type {import('./$types').PageData} */
        data: { t212Data: T212Data };
    }

    let { data }: Props = $props();
</script>

<main class="mx-10 mt-5">
    <InvestmentChart data={data.t212Data} />
</main>
