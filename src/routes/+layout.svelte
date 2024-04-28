<script lang="ts">
	import '../app.pcss';
	import Navbar from './Navbar.svelte'

    /** @type {import('./$types').PageData}*/
    export let data: { loggedIn: boolean, display_name: string };

</script>

<main class="w-screen h-screen">
	<Navbar {data} />
	<slot />
</main>
