import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { ColorSchemeScript, MantineProvider } from "@mantine/core";

export const Route = createRootRoute({
  component: () => (
    <>
      <MantineProvider defaultColorScheme="auto">
        <Outlet />
      </MantineProvider>
      <TanStackRouterDevtools />
    </>
  ),
});
