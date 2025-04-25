import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { MantineProvider } from "@mantine/core";
import { QueryClientProvider } from "@tanstack/react-query";
import queryClient from "~/lib/query";

export const Route = createRootRoute({
  component: () => (
    <>
      <MantineProvider defaultColorScheme="auto">
        <QueryClientProvider client={queryClient}>
          <Outlet />
          <ReactQueryDevtools />
        </QueryClientProvider>
      </MantineProvider>
      <TanStackRouterDevtools />
    </>
  ),
});
