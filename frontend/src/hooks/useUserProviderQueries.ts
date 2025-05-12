import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "~/lib/query";

// Types
export type Provider = {
  id: string;
  name: string;
  allow_custom_url: boolean;
};

export type Module = {
  id: number;
  name: string;
};

export type ProviderWithModules = Provider & {
  type: "oauth" | "token" | "basic";
  modules: Module[];
};

// Query keys
export const providerKeys = {
  all: ["providers"] as const,
  providers: () => [...providerKeys.all, "list"] as const,
  missingProviders: () => [...providerKeys.all, "missing"] as const,
  provider: (id: string) => [...providerKeys.all, "detail", id] as const,
};

// Query hooks
export const useProviders = () => {
  return useQuery({
    queryKey: providerKeys.providers(),
    queryFn: async () => {
      const { data } = await api.get<ProviderWithModules[]>("/user/providers");
      return data;
    },
  });
};

export const useMissingProviders = () => {
  return useQuery({
    queryKey: providerKeys.missingProviders(),
    queryFn: async () => {
      const { data } = await api.get<ProviderWithModules[]>(
        "/user/providers/missing",
      );
      return data;
    },
  });
};

// Mutation hooks
export const useAddOAuthProvider = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      providerId,
      code,
    }: {
      providerId: string;
      code: string;
    }) => {
      await api.post(`/user/providers/${providerId}/oauth_token?code=${code}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: providerKeys.all });
    },
  });
};

export const useAddTokenProvider = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      providerId,
      token,
      customUrl,
    }: {
      providerId: string;
      token: string;
      customUrl?: string;
    }) => {
      await api.post(`/user/providers/${providerId}/basic_token`, {
        token,
        custom_url: customUrl,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: providerKeys.all });
    },
  });
};

export const useUpdateTokenProvider = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      providerId,
      token,
      customUrl,
    }: {
      providerId: string;
      token: string;
      customUrl?: string;
    }) => {
      await api.patch(`/user/providers/${providerId}/basic_token`, {
        token,
        custom_url: customUrl,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: providerKeys.all });
    },
  });
};

export const useAddBasicProvider = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      providerId,
      username,
      password,
      customUrl,
    }: {
      providerId: string;
      username: string;
      password: string;
      customUrl?: string;
    }) => {
      await api.post(`/user/providers/${providerId}/basic_login`, {
        username,
        password,
        custom_url: customUrl,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: providerKeys.all });
    },
  });
};

export const useUpdateBasicProvider = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      providerId,
      username,
      password,
      customUrl,
    }: {
      providerId: string;
      username: string;
      password: string;
      customUrl?: string;
    }) => {
      await api.patch(`/user/providers/${providerId}/basic_login`, {
        username,
        password,
        custom_url: customUrl,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: providerKeys.all });
    },
  });
};

export const useRemoveProvider = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (providerId: string) => {
      await api.delete(`/user/providers/${providerId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: providerKeys.all });
    },
  });
};

export const useTestProviderConnection = () => {
  return useMutation({
    mutationFn: async (providerId: string) => {
      await api.post(`/user/providers/${providerId}/test`);
    },
  });
};
