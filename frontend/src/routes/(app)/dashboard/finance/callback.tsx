import { createFileRoute, redirect, useNavigate } from "@tanstack/react-router";
import { Center, Text, Loader, Alert, Button } from "@mantine/core";
import { api } from "~/lib/query";
import { IconAlertCircle } from "@tabler/icons-react";
import { useEffect } from "react";

// Define the type for the loader data
type CallbackLoaderData = {
  status: "loading" | "success" | "error";
  error?: string;
};

export const Route = createFileRoute("/(app)/dashboard/finance/callback")({
  // Use loader to handle the callback parameters and initiate the request
  loader: async (): Promise<CallbackLoaderData> => {
    // Get the current URL and extract the ref parameter
    const url = new URL(window.location.href);
    const ref = url.searchParams.get("ref");

    // If ref is missing, redirect to finance dashboard with error
    if (!ref) {
      throw redirect({
        to: "/dashboard/finance",
        search: { error: "Missing reference parameter" },
      });
    }

    try {
      // Make the API call directly in the loader
      const response = await api.post(`/finance/bank/callback?ref=${ref}`);

      // Return success status - we'll redirect in the component
      if (response.status === 200) {
        return { status: "success" };
      } else {
        return { status: "error", error: "Failed to add bank account" };
      }
    } catch (error) {
      // For errors, return error status to display in the component
      return {
        status: "error",
        error: (error as Error).message,
      };
    }
  },
  component: BankAccountCallback,
});

// Callback component
function BankAccountCallback() {
  const loaderData = Route.useLoaderData() as CallbackLoaderData;
  const navigate = useNavigate();

  // Use useEffect to handle redirection on success
  useEffect(() => {
    if (loaderData.status === "success") {
      navigate({ to: "/dashboard/finance" });
    }
  }, [loaderData.status, navigate]);

  // If there's an error, show an error message with a button to go back
  if (loaderData.status === "error") {
    return (
      <Center style={{ height: "100vh", flexDirection: "column" }}>
        <Alert
          icon={<IconAlertCircle size={16} />}
          title="Error"
          color="red"
          mb="md"
        >
          {loaderData.error || "Failed to add bank account"}
        </Alert>
        <Text mt="md" mb="lg">
          There was a problem processing your bank account connection.
        </Text>
        <Button onClick={() => navigate({ to: "/dashboard/finance" })}>
          Return to Finance Dashboard
        </Button>
      </Center>
    );
  }

  // Show loading state
  return (
    <Center style={{ height: "100vh", flexDirection: "column" }}>
      <Loader size="xl" />
      <Text mt="md">Processing your bank account connection...</Text>
      <Text mt="md" size="sm" c="dimmed">
        {loaderData.status === "success"
          ? "Success! Redirecting..."
          : "Please wait..."}
      </Text>
    </Center>
  );
}

export default BankAccountCallback;
