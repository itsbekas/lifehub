<script>
    /** @type {import('./$types').PageData}*/
    export let data;
</script>

<main>
    <h1>Checking Cash: {data.cash}€</h1>
    <h1>Invested Cash: {data.invested}€</h1>
    <h1>Uninvested Cash: {data.uninvested}€</h1>
    <h1>Returns: {data.returns}€</h1>
    <h1>Total: {data.total}€</h1>
</main>
