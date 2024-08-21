<script lang="ts">
    import SettingsSection from '$components/settings/SettingsSection.svelte';
    import SettingsTextInput from '$components/settings/SettingsTextInput.svelte';

    /** @type {import('./$types').PageData} */
    export let data: { user: User };

</script>

<SettingsSection
    title="Profile"
    description="Update your profile information."
>
    <SettingsTextInput
        title="Display Name"
        description="Your display name is how you appear to other users."
        value={data.user.name}
        autocomplete="name"
    />
    <SettingsTextInput
        title="Email Address"
        description="Your email address is used for account recovery and notifications."
        value={data.user.email}
        autocomplete="email"
    />
    <SettingsTextInput
        title="Change Password"
        description="Change your account password."
        type="password"
        autocomplete="new-password"
    />
    <SettingsTextInput
        title="Confirm Password"
        description="Confirm your new password."
        type="password"
        autocomplete="new-password"
    />
</SettingsSection>
