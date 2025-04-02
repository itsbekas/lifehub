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
import type { ActionFunction } from "react-router";

export const action: ActionFunction = async ({ request }) => {
  const formData = await request.formData();
  const username = formData.get("username") as string;
  const name = formData.get("name") as string;
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  try {
    const response = await fetch(
      `${process.env.BACKEND_URL}/api/v0/user/signup`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, name, email, password }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.message };
    }

    return redirect("/login");
  } catch (error) {
    console.error(error);
    return { error: "An unexpected error occurred." };
  }
};

const SignupPage = () => {
  const form = useForm({
    initialValues: {
      username: "",
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    },

    validate: {
      username: (value) => (value.trim() ? null : "Username is required"),
      name: (value) => (value.trim() ? null : "Name is required"),
      email: (value) =>
        /^\S+@\S+\.\S+$/.test(value) ? null : "Invalid email address",
      password: (value) =>
        value.trim().length >= 6
          ? null
          : "Password must be at least 6 characters",
      confirmPassword: (value, values) =>
        value === values.password ? null : "Passwords do not match",
    },
  });

  const actionData = useActionData<{ error?: string }>();

  return (
    <Center style={{ minHeight: "100vh" }}>
      <Card withBorder shadow="md" p={30} radius="md" style={{ width: 420 }}>
        <Title ta="center" order={2}>
          Create an Account
        </Title>
        <Text ta="center" size="sm" mt={5} c="dimmed">
          Sign up to start managing your dashboard
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
            label="Username"
            placeholder="Choose a username"
            name="username"
            {...form.getInputProps("username")}
            required
            mt={20}
            mb={15}
          />
          <TextInput
            label="Name"
            placeholder="Enter your display name"
            name="name"
            {...form.getInputProps("name")}
            required
            mb={15}
          />
          <TextInput
            label="Email"
            placeholder="Enter your email address"
            name="email"
            {...form.getInputProps("email")}
            required
            mb={15}
          />
          <PasswordInput
            label="Password"
            placeholder="Choose a password"
            name="password"
            {...form.getInputProps("password")}
            required
            mb={15}
          />
          <PasswordInput
            label="Confirm Password"
            placeholder="Confirm your password"
            name="confirmPassword"
            {...form.getInputProps("confirmPassword")}
            required
            mb={15}
          />
          {actionData?.error && (
            <Text c="red" size="sm" mt={5}>
              {actionData.error}
            </Text>
          )}
          {form.errors && (
            <Text c="red" size="sm" mt={5}>
              {Object.values(form.errors).join(", ")}
            </Text>
          )}
          <Button type="submit" fullWidth mt="md">
            Sign Up
          </Button>
        </Form>
        <Text ta="center" size="sm" mt="sm">
          Already have an account?{" "}
          <Text component="a" href="/login" c="blue">
            Log in
          </Text>
        </Text>
      </Card>
    </Center>
  );
};

export default SignupPage;
