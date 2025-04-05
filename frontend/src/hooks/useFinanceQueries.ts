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

export type Bank = {
  id: string;
  name: string;
  logo: string;
};

// Query keys
export const financeKeys = {
  all: ["finance"] as const,
  transactions: () => [...financeKeys.all, "transactions"] as const,
  categories: () => [...financeKeys.all, "categories"] as const,
  balances: () => [...financeKeys.all, "balances"] as const,
  banks: () => [...financeKeys.all, "banks"] as const,
};

// Query hooks
export const useTransactions = () => {
  return useQuery({
    queryKey: financeKeys.transactions(),
    queryFn: async () => {
      const { data } = await api.get<Transaction[]>(
        "/finance/bank/transactions",
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

// Mutation hooks
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
      queryClient.invalidateQueries({ queryKey: financeKeys.transactions() });
    },
  });
};
