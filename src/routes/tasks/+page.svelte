<script>
    /** @type {import('./$types').PageData}*/
    export let data;
</script>

<main>
    <h1>Dailies:</h1>
    <ul>
        {#each data.dailies as daily}
            <li>{daily.text}</li>
        {/each}
    </ul>
    <h1>Todos:</h1>
    <ul>
        {#each data.todos as todo}
            <li>{todo.text}</li>
        {/each}
    </ul>
    <h1>Habits:</h1>
    <ul>
        {#each data.habits as habit}
            <li>{habit.text}</li>
        {/each}
    </ul>
</main>