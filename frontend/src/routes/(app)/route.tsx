import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";
import { AppShell, Container } from "@mantine/core";
import { isAuthenticated } from "~/lib/cookies";
import { ErrorAlert } from "~/components/ErrorAlert";
import { Sidebar } from "~/components/Sidebar";

export const Route = createFileRoute("/(app)")({
  beforeLoad: () => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      throw redirect({ to: "/login" });
    }
  },
  loader: () => {
    const searchParams = new URLSearchParams(window.location.search);
    const error = searchParams.get("error");
    return { error };
  },
  component: DashboardLayout,
});

function DashboardLayout() {
  const { error } = Route.useLoaderData();

  return (
    <AppShell
      padding="md"
      navbar={{
        width: 80,
        breakpoint: "sm",
        collapsed: { desktop: false, mobile: true },
      }}
    >
      <AppShell.Navbar>
        <Sidebar />
      </AppShell.Navbar>
      <AppShell.Main mah="100vh">
        <Container fluid>
          <ErrorAlert error={error} />
          <Outlet />
        </Container>
      </AppShell.Main>
    </AppShell>
  );
}

export default DashboardLayout;
