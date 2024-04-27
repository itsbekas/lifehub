<script>
	import '../app.pcss';
	import Navbar from './Navbar.svelte'
</script>

<main class="w-screen h-screen">
	<Navbar />
	<slot />
</main>
