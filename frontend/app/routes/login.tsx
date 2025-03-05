import {
  Button,
  Card,
  Center,
  PasswordInput,
  Text,
  TextInput,
  Title,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { Form, redirect, useActionData } from "react-router";
import { getSession, commitSession } from "~/utils/session";
import type { ActionFunction } from "react-router";
import { data } from "react-router";
import type { Route } from "./+types/login";

export async function loader({ request }: Route.LoaderArgs) {
  const session = await getSession(request.headers.get("Cookie"));

  if (session.has("access_token")) {
    // Redirect to the home page if they are already signed in.
    return redirect("/");
  }

  return data(
    { error: session.get("error") },
    {
      headers: {
        "Set-Cookie": await commitSession(session),
      },
    }
  );
}

export const action: ActionFunction = async ({ request }) => {
  const formData = await request.formData();
  const username = formData.get("username") as string;
  const password = formData.get("password") as string;

  try {
    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/api/v0/user/login`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.message }; // Return error to the client
    }

    const { access_token, expires_at } = await response.json();

    // Create a session and store the token
    const session = await getSession();
    session.set("access_token", access_token);

    return new Response(null, {
      headers: {
        "Set-Cookie": await commitSession(session),
      },
    });
  } catch (error) {
    console.error(error);
    return { error: "An unexpected error occurred." };
  }
};

const LoginPage = () => {
  const form = useForm({
    initialValues: {
      username: "",
      password: "",
    },

    validate: {
      username: (value) => (value.trim() ? null : "Username is required"),
      password: (value) => (value.trim() ? null : "Password is required"),
    },
  });

  const actionData = useActionData<{ error?: string }>();

  return (
    <Center style={{ minHeight: "100vh" }}>
      <Card withBorder shadow="md" p={30} radius="md" style={{ width: 420 }}>
        <Title ta="center" order={2}>
          Welcome Back
        </Title>
        <Text ta="center" size="sm" mt={5} c="dimmed">
          Login to access your dashboard
        </Text>
        <Form
          method="post"
          onSubmit={(e) => {
            if (!form.validate().hasErrors) {
              return; // Allow submission
            }
            e.preventDefault(); // Prevent submission if validation fails
          }}
        >
          <TextInput
            label="Email or Username"
            placeholder="Enter your email or username"
            name="username"
            {...form.getInputProps("username")}
            required
            mt={20}
            mb={15}
          />
          <PasswordInput
            label="Password"
            placeholder="Your password"
            name="password"
            {...form.getInputProps("password")}
            required
            mb={15}
          />
          {actionData?.error && (
            <Text color="red" size="sm" mt={5}>
              {actionData.error}
            </Text>
          )}
          {form.errors && (
            <Text color="red" size="sm" mt={5}>
              {Object.values(form.errors).join(", ")}
            </Text>
          )}
          <Button type="submit" fullWidth mt="md">
            Login
          </Button>
        </Form>
        <Text ta="center" size="sm" mt="sm">
          Forgot your password?{" "}
          <Text component="a" href="#" c="blue">
            Reset it here
          </Text>
        </Text>
        <Text ta="center" size="sm" mt="sm">
          Don't have an account?{" "}
          <Text component="a" href="/signup" c="blue">
            Sign up
          </Text>
        </Text>
      </Card>
    </Center>
  );
};

export default LoginPage;
