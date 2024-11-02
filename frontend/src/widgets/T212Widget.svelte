<script lang="ts">
    import Widget from '$widgets/Widget.svelte';

    let { data } = $props();

</script>

<Widget title="Trading 212" href="/modules/finance/">
    <div class="flex flex-col space-y-2">
        <span>Account Value: {data.balance.free}</span>
        <span>Invested: {(data.balance.invested + data.balance.result).toFixed(2)} ({data.balance.result > 0 ? '+' : ''}{data.balance.result})</span>
        <span>Total: {data.balance.free + data.balance.invested + data.balance.result}</span>
    </div>
</Widget>
