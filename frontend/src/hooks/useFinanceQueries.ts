import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "~/lib/query";

// Types
export type Transaction = {
  id: string;
  account_id: string;
  amount: number;
  date: string;
  description: string;
  counterparty: string;
  subcategory_id: string;
  user_description: string;
};

export type PaginationInfo = {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
};

export type PaginatedResponse<T> = {
  items: T[];
  pagination: PaginationInfo;
};

export type SubCategory = {
  id: string;
  name: string;
  category_id: string;
  category_name: string;
  budgeted: number;
  spent: number;
  available: number;
};

export type Category = {
  id: string;
  name: string;
  subcategories: SubCategory[];
};

export type BankBalance = {
  bank: string;
  account_id: string;
  balance: number;
};

export type Country = {
  code: string;
  name: string;
};

export type Bank = {
  id: string;
  name: string;
  logo: string;
};

// Query keys
export const financeKeys = {
  all: ["finance"] as const,
  transactions: (page: number = 1, pageSize: number = 20) =>
    [...financeKeys.all, "transactions", { page, pageSize }] as const,
  categories: () => [...financeKeys.all, "categories"] as const,
  balances: () => [...financeKeys.all, "balances"] as const,
  banks: () => [...financeKeys.all, "banks"] as const,
  banksByCountry: (country: string) =>
    [...financeKeys.banks(), country] as const,
  countries: () => [...financeKeys.all, "countries"] as const,
};

// Query hooks
export const useTransactions = (page: number = 1, pageSize: number = 20) => {
  return useQuery({
    queryKey: financeKeys.transactions(page, pageSize),
    queryFn: async () => {
      // Use the paginated endpoint with query parameters
      const { data } = await api.get<PaginatedResponse<Transaction>>(
        `/finance/bank/transactions?page=${page}&page_size=${pageSize}`,
      );

      return data;
    },
  });
};

export const useCategories = () => {
  return useQuery({
    queryKey: financeKeys.categories(),
    queryFn: async () => {
      const { data } = await api.get<Category[]>("/finance/budget/categories");
      return data;
    },
  });
};

export const useBalances = () => {
  return useQuery({
    queryKey: financeKeys.balances(),
    queryFn: async () => {
      const { data } = await api.get<BankBalance[]>("/finance/bank/balances");
      return data;
    },
  });
};

export const useBanks = () => {
  return useQuery({
    queryKey: financeKeys.banks(),
    queryFn: async () => {
      const { data } = await api.get<Bank[]>("/finance/bank/banks");
      return data;
    },
  });
};

export const useCountries = () => {
  return useQuery({
    queryKey: financeKeys.countries(),
    queryFn: async () => {
      const { data } = await api.get<Country[]>("/finance/bank/countries");
      return data;
    },
  });
};

export const useBanksByCountry = (country: string) => {
  return useQuery({
    queryKey: financeKeys.banksByCountry(country),
    queryFn: async () => {
      const { data } = await api.get<Bank[]>(
        `/finance/bank/banks?country=${country}`,
      );
      return data;
    },
    enabled: !!country, // Only run the query if country is provided
  });
};

// Mutation hooks

// Hook for handling bank callback
export const useBankCallback = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (ref: string) => {
      const response = await api.post(`/finance/bank/callback?ref=${ref}`);
      return response.data;
    },
    onSuccess: () => {
      // Invalidate balances query to refresh the data
      queryClient.invalidateQueries({ queryKey: financeKeys.balances() });
    },
  });
};

export const useCreateCategory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (name: string) => {
      const { data } = await api.post("/finance/budget/categories", { name });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: financeKeys.categories() });
    },
  });
};

export const useCreateSubCategory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      name,
      amount,
      category_id,
    }: {
      name: string;
      amount: number;
      category_id: string;
    }) => {
      const { data } = await api.post(
        `/finance/budget/categories/${category_id}/subcategories`,
        {
          name,
          amount: parseFloat(amount.toString()),
        },
      );
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: financeKeys.categories() });
    },
  });
};

export const useAddBankAccount = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (bank_id: string) => {
      const { data } = await api.get<string>(
        `/finance/bank/login?bank_id=${bank_id}`,
      );
      return data; // This should be the login URL
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: financeKeys.balances() });
    },
  });
};

export const useEditTransaction = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      account_id,
      transaction_id,
      description,
      amount,
      subcategory_id,
    }: {
      account_id: string;
      transaction_id: string;
      description: string;
      amount: number;
      subcategory_id: string;
    }) => {
      const { data } = await api.put(
        `/finance/bank/${account_id}/transactions/${transaction_id}`,
        {
          description,
          subcategory_id,
          amount: parseFloat(amount.toString()),
        },
      );
      return data;
    },
    onSuccess: () => {
      // Invalidate both the regular and paginated transaction queries
      queryClient.invalidateQueries({ queryKey: financeKeys.transactions() });
      queryClient.invalidateQueries({
        predicate: (query) => {
          const queryKey = query.queryKey as unknown[];
          return (
            queryKey.length > 2 &&
            queryKey[0] === "finance" &&
            queryKey[1] === "transactions" &&
            typeof queryKey[2] === "object"
          );
        },
      });
    },
  });
};
