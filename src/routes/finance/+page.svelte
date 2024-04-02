<script>
    /** @type {import('./$types').PageData}*/
    export let data;
</script>

<main>
    <h1>Cash: {data.cash}€</h1>
    <h1>Investments: {data.investments}€</h1>
    <h1>Networth: {data.total}€</h1>
</main>
