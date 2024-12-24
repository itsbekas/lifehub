<script lang="ts">
  let {
    navbarItems = [
      {
        title: 'Dashboard',
        href: '/dashboard'
      },
      {
        title: 'Settings',
        href: '/settings/profile'
      }
    ]
  } = $props();
</script>

<div class="border-b border-gray-300 px-24 py-4 align-middle">
  <nav class="flex items-center justify-between hover:font-sans">
    <a href="/" class="text-3xl font-bold text-gray-800">Lifehub</a>
    <ul class="flex">
      {#each navbarItems as { title, href }}
        <li><a {href} class="ml-4 align-middle text-gray-600 hover:text-gray-800">{title}</a></li>
      {/each}
    </ul>
  </nav>
</div>
