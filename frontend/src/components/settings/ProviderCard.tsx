import { Card, Group, Text, Button, Stack } from "@mantine/core";
import { IconRefresh, IconTrash } from "@tabler/icons-react";
import {
  useRemoveProvider,
  useTestProviderConnection,
  type ProviderWithModules,
} from "~/hooks/useUserProviderQueries";
import { UpdateProviderModal } from "./UpdateProviderModal";

interface ProviderCardProps {
  provider: ProviderWithModules;
  isAvailable?: boolean;
}

export function ProviderCard({ provider, isAvailable }: ProviderCardProps) {
  const removeProvider = useRemoveProvider();
  const testConnection = useTestProviderConnection();

  const handleTest = () => {
    testConnection.mutate(provider.id);
  };

  const handleRemove = () => {
    removeProvider.mutate(provider.id);
  };

  return (
    <Card withBorder>
      <Group justify="space-between" wrap="nowrap">
        <Stack gap="xs">
          <Text fw={500}>{provider.name}</Text>
          <Text size="sm" c="dimmed">
            {provider.modules.map((m) => m.name).join(", ")}
          </Text>
        </Stack>

        <Group gap="xs">
          {isAvailable ? (
            <UpdateProviderModal provider={provider} />
          ) : (
            <>
              <Button
                variant="light"
                size="compact-sm"
                onClick={handleTest}
                loading={testConnection.isPending}
              >
                <IconRefresh size={16} />
              </Button>
              <UpdateProviderModal provider={provider} />
              <Button
                color="red"
                variant="light"
                size="compact-sm"
                onClick={handleRemove}
                loading={removeProvider.isPending}
              >
                <IconTrash size={16} />
              </Button>
            </>
          )}
        </Group>
      </Group>
    </Card>
  );
}
