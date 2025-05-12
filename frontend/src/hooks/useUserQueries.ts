import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "~/lib/query";

// Types
export type User = {
  id: string;
  username: string;
  email: string;
  name: string;
  created_at: string;
  verified: boolean;
  is_admin: boolean;
};

export type LoginRequest = {
  username: string;
  password: string;
};

export type SignupRequest = {
  username: string;
  email: string;
  password: string;
  name: string;
};

export type UpdateUserRequest = {
  name?: string;
  email?: string;
  password?: string;
};

export type UserToken = {
  name: string;
  access_token: string;
  expires_at: string;
};

// Query keys
export const userKeys = {
  all: ["user"] as const,
  me: () => [...userKeys.all, "me"] as const,
};

// Query hooks
export const useCurrentUser = () => {
  return useQuery({
    queryKey: userKeys.me(),
    queryFn: async () => {
      const { data } = await api.get<User>("/user/me");
      return data;
    },
  });
};

// Mutation hooks
export const useLogin = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (credentials: LoginRequest) => {
      const { data } = await api.post<UserToken>("/user/login", credentials);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.all });
    },
  });
};

export const useSignup = () => {
  return useMutation({
    mutationFn: async (userData: SignupRequest) => {
      await api.post("/user/signup", userData);
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (userData: UpdateUserRequest) => {
      const { data } = await api.patch<User>("/user/me", userData);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.me() });
    },
  });
};

export const useDeleteUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      await api.delete("/user/me");
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.all });
    },
  });
};

export const useVerifyEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (token: string) => {
      const { data } = await api.post<UserToken>("/user/verify-email", {
        token,
      });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.all });
    },
  });
};
