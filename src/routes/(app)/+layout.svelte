<script lang="ts">
	import '../../app.pcss';
	import Navbar from '../Navbar.svelte'

    /** @type {import('./$types').PageData}*/
    export let data: { hasToken: boolean, display_name: string };

	import { loggedIn } from '$lib/stores.js';

	loggedIn.set(data.hasToken);

</script>

<body class="w-screen h-screen">
	<Navbar {data}/>
	<main class="mx-10 mt-5">
		<slot />
	</main>
</body>
