import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, TextInput, Stack } from "@mantine/core";
import {
  useAddTokenProvider,
  useAddBasicProvider,
  type ProviderWithModules,
} from "~/hooks/useUserProviderQueries";

interface AddProviderModalProps {
  provider: ProviderWithModules;
}

export function AddProviderModal({ provider }: AddProviderModalProps) {
  const [opened, { open, close }] = useDisclosure(false);
  const [token, setToken] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [customUrl, setCustomUrl] = useState("");

  const addTokenProvider = useAddTokenProvider();
  const addBasicProvider = useAddBasicProvider();

  const handleSubmit = async () => {
    if (provider.type === "token") {
      await addTokenProvider.mutateAsync({
        providerId: provider.id,
        token,
        customUrl: customUrl || undefined,
      });
    } else if (provider.type === "basic") {
      await addBasicProvider.mutateAsync({
        providerId: provider.id,
        username,
        password,
        customUrl: customUrl || undefined,
      });
    } else if (provider.type === "oauth") {
      // OAuth providers are handled differently - they redirect to the provider's auth page
      window.location.href = `/api/user/providers/${provider.id}/oauth_url`;
      return;
    }

    close();
    setToken("");
    setUsername("");
    setPassword("");
    setCustomUrl("");
  };

  return (
    <>
      <Modal opened={opened} onClose={close} title={`Connect ${provider.name}`}>
        <Stack>
          {provider.type === "token" && (
            <TextInput
              label="API Token"
              value={token}
              onChange={(e) => setToken(e.currentTarget.value)}
              required
            />
          )}

          {provider.type === "basic" && (
            <>
              <TextInput
                label="Username"
                value={username}
                onChange={(e) => setUsername(e.currentTarget.value)}
                required
              />
              <TextInput
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.currentTarget.value)}
                required
              />
            </>
          )}

          {provider.allow_custom_url && (
            <TextInput
              label="Custom URL"
              value={customUrl}
              onChange={(e) => setCustomUrl(e.currentTarget.value)}
              placeholder="https://api.example.com"
            />
          )}

          <Button
            onClick={handleSubmit}
            loading={addTokenProvider.isPending || addBasicProvider.isPending}
          >
            Connect
          </Button>
        </Stack>
      </Modal>

      <Button onClick={open} variant="light">
        Connect
      </Button>
    </>
  );
}
