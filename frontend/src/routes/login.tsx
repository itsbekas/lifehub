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
import { loginUser, isAuthenticated } from "~/lib/cookies";

// Define the login response type
interface LoginResponse {
  access_token: string;
  expires_at: string;
}

// Create the route using Tanstack Router
export const Route = createFileRoute("/login")({
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const [loginError, setLoginError] = useState<string | null>(null);

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
      password: "",
    },
    validate: {
      username: (value) => (value.trim() ? null : "Username is required"),
      password: (value) => (value.trim() ? null : "Password is required"),
    },
  });

  // Setup login mutation using React Query
  const loginMutation = useMutation({
    mutationFn: async (credentials: { username: string; password: string }) => {
      const response = await api.post<LoginResponse>(
        "/user/login",
        credentials,
      );
      return response.data;
    },
    onSuccess: (data) => {
      // Store the token in cookies
      loginUser(data.access_token, new Date(data.expires_at));
      // Navigate to dashboard
      navigate({ to: "/dashboard" });
    },
    onError: (
      error: Error & { response?: { data?: { message?: string } } },
    ) => {
      // Handle login error
      setLoginError(
        error.response?.data?.message ||
          "Login failed. Please check your credentials.",
      );
    },
  });

  // Handle form submission
  const handleSubmit = form.onSubmit((values) => {
    setLoginError(null); // Clear previous errors
    loginMutation.mutate(values);
  });

  return (
    <Center style={{ minHeight: "100vh" }}>
      <Card withBorder shadow="md" p={30} radius="md" style={{ width: 420 }}>
        <Title ta="center" order={2}>
          Welcome Back
        </Title>
        <Text ta="center" size="sm" mt={5} c="dimmed">
          Login to access your dashboard
        </Text>
        <form onSubmit={handleSubmit}>
          <TextInput
            label="Email or Username"
            placeholder="Enter your email or username"
            {...form.getInputProps("username")}
            required
            mt={20}
            mb={15}
          />
          <PasswordInput
            label="Password"
            placeholder="Your password"
            {...form.getInputProps("password")}
            required
            mb={15}
          />
          {loginError && (
            <Text c="red" size="sm" mt={5}>
              {loginError}
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
            loading={loginMutation.isPending}
          >
            {loginMutation.isPending ? "Logging in..." : "Login"}
          </Button>
        </form>
        <Text ta="center" size="sm" mt="sm">
          Forgot your password?{" "}
          <Text component="a" href="#" c="blue">
            Reset it here
          </Text>
        </Text>
        <Text ta="center" size="sm" mt="sm">
          Don't have an account?{" "}
          <Text
            component="a"
            onClick={() => navigate({ to: "/signup" })}
            style={{ cursor: "pointer" }}
            c="blue"
          >
            Sign up
          </Text>
        </Text>
      </Card>
    </Center>
  );
}

export default LoginPage;
