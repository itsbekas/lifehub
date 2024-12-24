<script lang="ts">
  import UserProviderCard from '@/components/settings/providers/UserProviderCard.svelte';
  import MissingProviderCard from '@/components/settings/providers/MissingProviderCard.svelte';
  import SettingsSection from '@/components/settings/SettingsSection.svelte';

  import type { Provider } from '@/lib/types/core';

  interface Props {
    /** @type {import('./$types').PageData}*/
    data: { missingProviders: Array<Provider>; userProviders: Array<Provider> };
  }

  let { data }: Props = $props();
</script>

<SettingsSection
  title="Your Providers"
  description="These are the providers you have connected to your account."
>
  {#if data.userProviders.length == 0}
    <p>You haven't connected any providers yet.</p>
  {:else}
    {#each data.userProviders as provider}
      <div class="mb-2">
        <UserProviderCard {provider} />
      </div>
    {/each}
  {/if}
</SettingsSection>

<SettingsSection title="Connect a Provider" description="Connect a new provider to your account.">
  {#if data.missingProviders.length == 0}
    <p>You've connected all available providers.</p>
  {:else}
    {#each data.missingProviders as provider}
      <div class="mb-2">
        <MissingProviderCard {provider} />
      </div>
    {/each}
  {/if}
</SettingsSection>
