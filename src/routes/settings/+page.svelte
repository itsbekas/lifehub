<script lang="ts">
    import SidebarNav from "$components/settings/SidebarNav.svelte";
    import SettingsPage from "$components/settings/SettingsPage.svelte";

	const sidebarNavItems = [
		{
			title: "Profile",
			href: "/examples/forms",
		},
		{
			title: "Account",
			href: "/examples/forms/account",
		},
		{
			title: "Appearance",
			href: "/examples/forms/appearance",
		},
		{
			title: "Notifications",
			href: "/examples/forms/notifications",
		},
		{
			title: "Display",
			href: "/examples/forms/display",
		},
	];
</script>

<div class="flex flex-row">
    <div class="w-60">
        <SidebarNav />
    </div>
    <SettingsPage />
</div>
