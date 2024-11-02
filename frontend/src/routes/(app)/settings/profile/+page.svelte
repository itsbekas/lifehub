<script lang="ts">
    import SettingsSection from '@/components/settings/SettingsSection.svelte';
    import SettingsTextInput from '@/components/settings/SettingsTextInput.svelte';

    
    interface Props {
        /** @type {import('./$types').PageData} */
        data: { user: User };
    }

    let { data }: Props = $props();

</script>

<SettingsSection
    title="Profile"
    description="Update your profile information."
>
    <form method="POST" action="?/updateProfile">
        <SettingsTextInput
            title="Display Name"
            description="Your display name is how you appear to other users."
            name="name"
            value={data.user.name}
            autocomplete="name"
        />
        <SettingsTextInput
            title="Email Address"
            description="Your email address is used for account recovery and notifications."
            name="email"
            value={data.user.email}
            autocomplete="email"
        />
        <SettingsTextInput
            title="Change Password"
            description="Change your account password."
            name="password"
            type="password"
            autocomplete="new-password"
        />
        <SettingsTextInput
            title="Confirm Password"
            description="Confirm your new password."
            name="password_confirm"
            type="password"
            autocomplete="new-password"
        />
        <button class="bg-blue-500 text-white font-semibold rounded-lg p-2 w-2/3 hover:bg-blue-600" type="submit">
            Save Changes
        </button>
    </form>
</SettingsSection>
