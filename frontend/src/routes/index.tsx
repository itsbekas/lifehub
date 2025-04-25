import { Center, Title, Button, Text } from "@mantine/core";
import { isAuthenticated } from "~/lib/cookies";
import { useNavigate, createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: () => {
    return <Home loggedIn={isAuthenticated()} />;
  },
});

export default function Home({ loggedIn }: { loggedIn: boolean }) {
  const navigate = useNavigate();

  return (
    <Center style={{ height: "100vh", flexDirection: "column" }}>
      <Title order={1} style={{ fontSize: "8rem" }}>
        Lifehub
      </Title>
      <Button
        style={{ marginTop: "2rem" }}
        onClick={() => navigate({ to: loggedIn ? "/dashboard" : "/login" })}
      >
        {loggedIn ? "Go to Dashboard" : "Login"}
      </Button>
      {!loggedIn && (
        <Text ta="center" size="sm" mt="sm">
          New here?{" "}
          <Text component="a" href="/signup" c="blue">
            Sign up
          </Text>
        </Text>
      )}
    </Center>
  );
}
