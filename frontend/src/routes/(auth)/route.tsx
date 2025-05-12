import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";
import { isAuthenticated } from "~/lib/cookies";

export const Route = createFileRoute("/(auth)")({
  beforeLoad: () => {
    if (isAuthenticated()) {
      throw redirect({ to: "/dashboard" });
    }
  },
  component: AuthLayout,
});

function AuthLayout() {
  return <Outlet />;
}

export default AuthLayout;
