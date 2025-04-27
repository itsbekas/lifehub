import { useState } from 'react';
import { useDisclosure } from '@mantine/hooks';
import { Modal, Button, TextInput, Stack } from '@mantine/core';
import { IconPencil } from '@tabler/icons-react';
import { 
  useUpdateTokenProvider, 
  useUpdateBasicProvider, 
  type ProviderWithModules 
} from '~/hooks/useUserProviderQueries';

interface UpdateProviderModalProps {
  provider: ProviderWithModules;
}

export function UpdateProviderModal({ provider }: UpdateProviderModalProps) {
  const [opened, { open, close }] = useDisclosure(false);
  const [token, setToken] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [customUrl, setCustomUrl] = useState('');

  const updateTokenProvider = useUpdateTokenProvider();
  const updateBasicProvider = useUpdateBasicProvider();

  const handleSubmit = async () => {
    if (provider.type === 'token') {
      await updateTokenProvider.mutateAsync({
        providerId: provider.id,
        token,
        customUrl: customUrl || undefined,
      });
    } else if (provider.type === 'basic') {
      await updateBasicProvider.mutateAsync({
        providerId: provider.id,
        username,
        password,
        customUrl: customUrl || undefined,
      });
    }
    
    close();
    setToken('');
    setUsername('');
    setPassword('');
    setCustomUrl('');
  };

  return (
    <>
      <Modal opened={opened} onClose={close} title={`Update ${provider.name}`}>
        <Stack>
          {provider.type === 'token' && (
            <TextInput
              label="API Token"
              value={token}
              onChange={(e) => setToken(e.currentTarget.value)}
              required
            />
          )}

          {provider.type === 'basic' && (
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
            loading={updateTokenProvider.isPending || updateBasicProvider.isPending}
          >
            Update
          </Button>
        </Stack>
      </Modal>

      <Button onClick={open} variant="light" size="compact-sm">
        <IconPencil size={16} />
      </Button>
    </>
  );
}