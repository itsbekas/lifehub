import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";
import { AppShell, Container } from "@mantine/core";
import { isAuthenticated } from "~/lib/cookies";
import { ErrorAlert } from "~/components/ErrorAlert";
import { Sidebar } from "~/components/Sidebar";
import classes from "~/styles/AppLayout.module.css";

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
    <AppShell navbar={{ width: 250, breakpoint: "sm" }} padding="md">
      <AppShell.Navbar>
        <Sidebar />
      </AppShell.Navbar>

      <AppShell.Main className={classes.main}>
        <Container size="xl">
          <ErrorAlert error={error} />
          <Outlet />
        </Container>
      </AppShell.Main>
    </AppShell>
  );
}

export default DashboardLayout;
