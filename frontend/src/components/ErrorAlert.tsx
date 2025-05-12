import { Alert } from "@mantine/core";
import { IconAlertCircle } from "@tabler/icons-react";

interface ErrorAlertProps {
  error: string | null;
}

export function ErrorAlert({ error }: ErrorAlertProps) {
  if (!error) return null;

  return (
    <Alert
      icon={<IconAlertCircle size={16} />}
      title="Error"
      color="red"
      mb="md"
      withCloseButton
      onClose={() => {
        // Remove the error parameter from the URL without navigation
        const url = new URL(window.location.href);
        url.searchParams.delete("error");
        window.history.replaceState({}, "", url);
      }}
    >
      {error}
    </Alert>
  );
}
