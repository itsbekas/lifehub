import {
  Outlet,
  createFileRoute,
  redirect,
} from "@tanstack/react-router";
import { HeaderMenu } from "~/components/HeaderMenu";
import { Container } from "@mantine/core";
import { isAuthenticated } from "~/lib/cookies";

export const Route = createFileRoute("/dashboard")({
  beforeLoad: () => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      throw redirect({ to: "/login" });
    }
  },
  component: DashboardLayout,
});

function DashboardLayout() {
  return (
    <div>
      <HeaderMenu />
      <Container size="lg" style={{ paddingTop: "1rem" }}>
        <Outlet />
      </Container>
    </div>
  );
}

export default DashboardLayout;
