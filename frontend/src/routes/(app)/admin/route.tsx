import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";
import { api } from "~/lib/query";
import { Container } from "@mantine/core";

export const Route = createFileRoute("/(app)/admin")({
  beforeLoad: async () => {
    try {
      const response = await api.get("/user/me");
      if (!response.data.is_admin) {
        throw redirect({ to: "/dashboard" });
      }
    } catch {
      // If the API call fails or user is not admin, redirect to dashboard
      throw redirect({ to: "/dashboard" });
    }
  },
  component: AdminLayout,
});

function AdminLayout() {
  return (
    <Container size="xl">
      <Outlet />
    </Container>
  );
}

export default AdminLayout;
