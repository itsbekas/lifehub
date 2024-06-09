<script lang="ts">
    import Widget from '$widgets/Widget.svelte';

    export let data;

</script>

<Widget title="Trading 212" href="/modules/finance/">
    <div class="flex flex-col space-y-2">
        <span>Account Value: {data.balance.free}</span>
        <span>Invested: {data.balance.invested}</span>
        <span>Result: {data.balance.result}</span>
    </div>
</Widget>