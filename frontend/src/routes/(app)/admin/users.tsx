import { createFileRoute } from "@tanstack/react-router";
import { Title } from "@mantine/core";
import { UsersTable } from "~/components/UsersTable";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "~/api/admin";

export const Route = createFileRoute("/(app)/admin/users")({
  component: UsersPage,
});

function UsersPage() {
  const { data: users = [], isLoading } = useQuery({
    queryKey: ["admin", "users"],
    queryFn: () => adminApi.getAllUsers(),
  });

  return (
    <>
      <Title order={2} mb="md">
        Users
      </Title>
      {!isLoading && <UsersTable users={users} />}
    </>
  );
}

export default UsersPage;
