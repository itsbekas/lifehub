import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";
import { HeaderMenu } from "~/components/HeaderMenu";
import { Container } from "@mantine/core";
import { isAuthenticated } from "~/lib/cookies";
import { ErrorAlert } from "~/components/ErrorAlert";

export const Route = createFileRoute("/dashboard")({
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
    <div>
      <HeaderMenu />
      <Container size="lg" style={{ paddingTop: "1rem" }}>
        <ErrorAlert error={error} />
        <Outlet />
      </Container>
    </div>
  );
}

export default DashboardLayout;
