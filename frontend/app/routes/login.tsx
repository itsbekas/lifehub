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
import { accessTokenCookie } from "~/utils/cookies";
import type { ActionFunction } from "react-router";

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

    // Set the token in cookies
    return redirect("/dashboard", {
      headers: {
        "Set-Cookie": await accessTokenCookie.serialize(access_token, {
          expires: new Date(expires_at),
        }),
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
          <Text component="a" href="#" color="blue">
            Reset it here
          </Text>
        </Text>
      </Card>
    </Center>
  );
};

export default LoginPage;
