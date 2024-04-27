<script>
    export let provider;

    function handleClick() {
        // Handle click event here
    }
</script>

<button class="provider-card" on:click={handleClick}>
    <h3>{provider.name}</h3>
    <p>ID: {provider.id}</p>
    <p>Type: {provider.type}</p>
</button>

<style>
    .provider-card {
        border: 1px solid #ccc;
        padding: 10px;
        margin-bottom: 10px;
        cursor: pointer;
        outline: inherit;
        cursor: pointer;
        font: inherit;
        padding: 0;
        border: none;
        color: inherit;
        background: none;
    }
</style>