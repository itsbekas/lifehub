<script>

    let total = 0;

    async function fetchNetworth() {
        const res = await fetch('http://localhost:8000/finance/networth');
        const data = await res.json();
        total = data.total;
    }

</script>

<main>
    <h1>Networth: ${total}</h1>
    <button on:click={fetchNetworth}>Refresh</button>
</main>
