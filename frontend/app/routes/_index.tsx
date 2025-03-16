import { Center, Title, Button, Text } from "@mantine/core";
import { useNavigate } from "react-router";
import { isLoggedIn } from "~/utils/session";
import type { Route } from "./+types/_index";

export async function loader({ request }: Route.LoaderArgs) {
  return { loggedIn: await isLoggedIn(request) };
}

export default function Home({ loaderData }: Route.ComponentProps) {
  const { loggedIn } = loaderData;
  const navigate = useNavigate();

  return (
    <Center style={{ height: "100vh", flexDirection: "column" }}>
      <Title order={1} style={{ fontSize: "8rem" }}>
        Lifehub
      </Title>
      <Button
        style={{ marginTop: "2rem" }}
        onClick={() => navigate(loggedIn ? "/dashboard" : "/login")}
      >
        {loggedIn ? "Go to Dashboard" : "Login"}
      </Button>
      { !loggedIn &&
        <Text ta="center" size="sm" mt="sm">
          New here?{" "}
          <Text component="a" href="/signup" c="blue">
            Sign up
          </Text>
        </Text>
      }
    </Center>
  );
}
