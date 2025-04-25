import { useState } from "react";
import cx from "clsx";
import { ScrollArea, Table, Badge, Button } from "@mantine/core";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { adminApi } from "~/api/admin";
import classes from "~/styles/TransactionsTable.module.css";

type User = {
  id: string;
  username: string;
  email: string;
  name: string;
  created_at: string;
  verified: boolean;
  is_admin: boolean;
};

type UsersTableProps = {
  users: User[];
};

export function UsersTable({ users }: UsersTableProps) {
  const [scrolled, setScrolled] = useState(false);
  const queryClient = useQueryClient();

  const verifyMutation = useMutation({
    mutationFn: (userId: string) => adminApi.verifyUser(userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
    },
  });
  
  // Sort users by creation date, newest first
  const sortedUsers = [...users].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  // Format date to DD-MM-YYYY
  const formatDate = (date: string) => {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();
    return `${day}-${month}-${year}`;
  };

  const rows = sortedUsers.map((user) => (
    <Table.Tr key={user.id}>
      <Table.Td>{user.username}</Table.Td>
      <Table.Td>{user.name}</Table.Td>
      <Table.Td>{user.email}</Table.Td>
      <Table.Td>{formatDate(user.created_at)}</Table.Td>
      <Table.Td>
        <Badge color={user.verified ? "green" : "red"}>
          {user.verified ? "Verified" : "Unverified"}
        </Badge>
      </Table.Td>
      <Table.Td>
        <Badge color={user.is_admin ? "blue" : "gray"}>
          {user.is_admin ? "Admin" : "User"}
        </Badge>
      </Table.Td>
      <Table.Td>
        {!user.verified && (
          <Button
            size="xs"
            variant="light"
            color="blue"
            onClick={() => verifyMutation.mutate(user.id)}
            loading={verifyMutation.isPending}
          >
            Verify
          </Button>
        )}
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <ScrollArea.Autosize
      h={500}
      onScrollPositionChange={({ y }) => setScrolled(y !== 0)}
    >
      <Table>
        <Table.Thead
          className={cx(classes.header, { [classes.scrolled]: scrolled })}
        >
          <Table.Tr>
            <Table.Th>Username</Table.Th>
            <Table.Th>Name</Table.Th>
            <Table.Th>Email</Table.Th>
            <Table.Th>Created At</Table.Th>
            <Table.Th>Status</Table.Th>
            <Table.Th>Role</Table.Th>
            <Table.Th>Actions</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </ScrollArea.Autosize>
  );
}
