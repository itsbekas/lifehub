import {
  Container,
  Title,
  Stack,
  Card,
  Group,
  Text,
  LoadingOverlay,
} from "@mantine/core";
import {
  useProviders,
  useMissingProviders,
} from "~/hooks/useUserProviderQueries";
import { AddProviderModal } from "~/components/settings/AddProviderModal";
import { ProviderCard } from "~/components/settings/ProviderCard";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/(app)/settings/")({
  component: SettingsPage,
});

export default function SettingsPage() {
  const { data: providers, isLoading: isLoadingProviders } = useProviders();
  const { data: missingProviders, isLoading: isLoadingMissing } =
    useMissingProviders();

  return (
    <Container size="sm">
      <Stack gap="xl">
        <Title order={2}>Settings</Title>

        <Stack gap="md">
          <Group justify="space-between" align="center">
            <Title order={3}>Connected Providers</Title>
          </Group>

          <Card withBorder pos="relative">
            <LoadingOverlay visible={isLoadingProviders} />
            {providers?.length === 0 ? (
              <Text c="dimmed" ta="center" py="xl">
                No providers connected yet
              </Text>
            ) : (
              <Stack gap="md">
                {providers?.map((provider) => (
                  <ProviderCard key={provider.id} provider={provider} />
                ))}
              </Stack>
            )}
          </Card>

          <Title order={3} mt="xl">
            Available Providers
          </Title>
          <Card withBorder pos="relative">
            <LoadingOverlay visible={isLoadingMissing} />
            {missingProviders?.length === 0 ? (
              <Text c="dimmed" ta="center" py="xl">
                No additional providers available
              </Text>
            ) : (
              <Stack gap="md">
                {missingProviders?.map((provider) => (
                  <Card key={provider.id} withBorder>
                    <Group justify="space-between" wrap="nowrap">
                      <Stack gap="xs">
                        <Text fw={500}>{provider.name}</Text>
                        <Text size="sm" c="dimmed">
                          {provider.modules.map(m => m.name).join(', ')}
                        </Text>
                      </Stack>
                      <AddProviderModal provider={provider} />
                    </Group>
                  </Card>
                ))}
              </Stack>
            )}
          </Card>
        </Stack>
      </Stack>
    </Container>
  );
}
