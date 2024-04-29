<script lang="ts">
	import '../app.pcss';
	import Navbar from './Navbar.svelte'

    /** @type {import('./$types').PageData}*/
    export let data: { hasToken: boolean, display_name: string };

	import { loggedIn } from '$lib/stores.js';

	loggedIn.set(data.hasToken);

</script>

<main class="w-screen h-screen">
	<Navbar {data} />
	<slot />
</main>
