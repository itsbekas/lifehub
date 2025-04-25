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
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useMutation } from "@tanstack/react-query";
import { useState, useEffect } from "react";
import { api } from "~/lib/query";
import { isAuthenticated } from "~/lib/cookies";

// Define the signup request type
interface SignupRequest {
  username: string;
  name: string;
  email: string;
  password: string;
}

// Create the route using Tanstack Router
export const Route = createFileRoute("/signup")({
  component: SignupPage,
});

function SignupPage() {
  const navigate = useNavigate();
  const [signupError, setSignupError] = useState<string | null>(null);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated()) {
      navigate({ to: "/dashboard" });
    }
  }, [navigate]);

  // Setup form with validation
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

  // Setup signup mutation using React Query
  const signupMutation = useMutation({
    mutationFn: async (userData: SignupRequest) => {
      const response = await api.post("/user/signup", userData);
      return response.data;
    },
    onSuccess: () => {
      // Navigate to login page after successful signup
      navigate({ to: "/login" });
    },
    onError: (
      error: Error & { response?: { data?: { message?: string } } },
    ) => {
      // Handle signup error
      setSignupError(
        error.response?.data?.message || "Signup failed. Please try again.",
      );
    },
  });

  // Handle form submission
  const handleSubmit = form.onSubmit((values) => {
    setSignupError(null); // Clear previous errors

    // Extract the fields needed for the API request
    const { username, name, email, password } = values;
    signupMutation.mutate({ username, name, email, password });
  });

  return (
    <Center style={{ minHeight: "100vh" }}>
      <Card withBorder shadow="md" p={30} radius="md" style={{ width: 420 }}>
        <Title ta="center" order={2}>
          Create an Account
        </Title>
        <Text ta="center" size="sm" mt={5} c="dimmed">
          Sign up to start managing your dashboard
        </Text>
        <form onSubmit={handleSubmit}>
          <TextInput
            label="Username"
            placeholder="Choose a username"
            {...form.getInputProps("username")}
            required
            mt={20}
            mb={15}
          />
          <TextInput
            label="Name"
            placeholder="Enter your display name"
            {...form.getInputProps("name")}
            required
            mb={15}
          />
          <TextInput
            label="Email"
            placeholder="Enter your email address"
            {...form.getInputProps("email")}
            required
            mb={15}
          />
          <PasswordInput
            label="Password"
            placeholder="Choose a password"
            {...form.getInputProps("password")}
            required
            mb={15}
          />
          <PasswordInput
            label="Confirm Password"
            placeholder="Confirm your password"
            {...form.getInputProps("confirmPassword")}
            required
            mb={15}
          />
          {signupError && (
            <Text c="red" size="sm" mt={5}>
              {signupError}
            </Text>
          )}
          {Object.values(form.errors).length > 0 && (
            <Text c="red" size="sm" mt={5}>
              {Object.values(form.errors).join(", ")}
            </Text>
          )}
          <Button
            type="submit"
            fullWidth
            mt="md"
            loading={signupMutation.isPending}
          >
            {signupMutation.isPending ? "Creating Account..." : "Sign Up"}
          </Button>
        </form>
        <Text ta="center" size="sm" mt="sm">
          Already have an account?{" "}
          <Text
            component="a"
            onClick={() => navigate({ to: "/login" })}
            style={{ cursor: "pointer" }}
            c="blue"
          >
            Log in
          </Text>
        </Text>
      </Card>
    </Center>
  );
}

export default SignupPage;
