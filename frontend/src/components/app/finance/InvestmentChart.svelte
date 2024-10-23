<script lang="ts">
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';

    /** type {import('./types').PageData}*/
    export let data: { history: Array<T212Transaction> };
    
    let cumulativeData: Array<T212Transaction> = data.history.reduce((acc: Array<T212Transaction>, transaction: T212Transaction) => {
        if (acc.length === 0) {
            return [transaction];
        }
        const lastTransaction = acc[acc.length - 1];
        const newTransaction = {
            ...transaction,
            amount: transaction.amount + lastTransaction.amount
        };
        return [...acc, newTransaction];
    }, []);

    let chartOptions = {
        xAxis: {
            data: cumulativeData.map(transaction => transaction.timestamp)
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: cumulativeData.map(transaction => transaction.amount),
            type: 'line'
        }]
    };

    onMount(() => {
        const chart = echarts.init(document.getElementById('chart'));
        chart.setOption(chartOptions);
    });

</script>

<main class="mx-10 mt-5">
    <div id="chart" style="width: 100%; height: 600px;"></div>
</main>