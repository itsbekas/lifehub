import {
  Container,
  Title,
  Stack,
  Card,
  Group,
  Text,
  Button,
  Modal,
  TextInput,
  PasswordInput,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useState } from "react";
import { useNavigate, createFileRoute } from "@tanstack/react-router";
import {
  useCurrentUser,
  useUpdateUser,
  useDeleteUser,
} from "~/hooks/useUserQueries";
import { logoutUser } from "~/lib/cookies";

export const Route = createFileRoute("/(app)/profile/")({
  component: ProfilePage,
});

export default function ProfilePage() {
  const { data: user } = useCurrentUser();
  const updateUser = useUpdateUser();
  const deleteUser = useDeleteUser();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [opened, { open, close }] = useDisclosure(false);
  const [deleteConfirmation, setDeleteConfirmation] = useState("");

  // Initialize form values when user data is loaded
  useState(() => {
    if (user) {
      setName(user.name || "");
      setEmail(user.email || "");
    }
  });

  const handleUpdateProfile = async () => {
    if (password && password !== confirmPassword) {
      // Handle password mismatch
      return;
    }

    const updateData = {
      name,
      email,
      ...(password ? { password } : {}),
    };

    await updateUser.mutateAsync(updateData);
  };

  const handleDeleteAccount = async () => {
    if (deleteConfirmation !== user?.username) {
      return;
    }

    await deleteUser.mutateAsync();
    logoutUser();
    navigate({ to: "/login" });
  };

  return (
    <Container size="sm">
      <Stack gap="xl">
        <Title order={2}>Profile</Title>

        <Card withBorder>
          <Stack gap="md">
            <Title order={3}>Account Information</Title>

            <TextInput label="Username" value={user?.username || ""} disabled />

            <TextInput
              label="Name"
              value={name}
              onChange={(e) => setName(e.currentTarget.value)}
            />

            <TextInput
              label="Email"
              value={email}
              onChange={(e) => setEmail(e.currentTarget.value)}
            />

            <Title order={4} mt="md">
              Change Password
            </Title>

            <PasswordInput
              label="New Password"
              value={password}
              onChange={(e) => setPassword(e.currentTarget.value)}
              placeholder="Leave blank to keep current password"
            />

            <PasswordInput
              label="Confirm New Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.currentTarget.value)}
              placeholder="Confirm your new password"
            />

            <Group justify="flex-end" mt="md">
              <Button
                onClick={handleUpdateProfile}
                loading={updateUser.isPending}
              >
                Update Profile
              </Button>
            </Group>
          </Stack>
        </Card>

        <Card withBorder>
          <Stack gap="md">
            <Title order={3} c="red">
              Danger Zone
            </Title>
            <Text size="sm">
              Deleting your account is permanent and cannot be undone. All your
              data will be removed.
            </Text>

            <Group justify="flex-end">
              <Button color="red" onClick={open}>
                Delete Account
              </Button>
            </Group>
          </Stack>
        </Card>
      </Stack>

      <Modal opened={opened} onClose={close} title="Delete Account" centered>
        <Stack gap="md">
          <Text size="sm">
            This action cannot be undone. All your data will be permanently
            deleted. To confirm, please type your username:{" "}
            <strong>{user?.username}</strong>
          </Text>

          <TextInput
            placeholder="Enter your username"
            value={deleteConfirmation}
            onChange={(e) => setDeleteConfirmation(e.currentTarget.value)}
          />

          <Button
            color="red"
            fullWidth
            onClick={handleDeleteAccount}
            loading={deleteUser.isPending}
            disabled={deleteConfirmation !== user?.username}
          >
            Permanently Delete Account
          </Button>
        </Stack>
      </Modal>
    </Container>
  );
}
