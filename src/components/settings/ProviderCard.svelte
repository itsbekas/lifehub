<script lang="ts">
    import SettingsCard from '$components/settings/SettingsCard.svelte';
    import { Dialog } from 'bits-ui';

    export let provider: Provider;
</script>

<SettingsCard>
    <div class="flex justify-between">
    <p>{ provider.name }</p>
    <Dialog.Root>
        <Dialog.Trigger>
            Delete
        </Dialog.Trigger>
        <Dialog.Portal>
          <Dialog.Overlay />
          <Dialog.Content>
            <Dialog.Title />
            <Dialog.Description />
            <Dialog.Close />
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
</SettingsCard>
