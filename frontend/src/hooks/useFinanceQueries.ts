import {
  useMutation,
  useQuery,
  useQueryClient,
  useInfiniteQuery,
} from "@tanstack/react-query";
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
  monthly_income: number;
  monthly_expenses: number;
  monthly_last_updated: string | null;
};

export type Country = {
  code: string;
  name: string;
};

export type Bank = {
  id: string;
  type: string;
  name: string;
  logo: string;
};

// Query keys
export const financeKeys = {
  all: ["finance"] as const,
  transactions: (page: number = 1, pageSize: number = 20) =>
    [...financeKeys.all, "transactions", { page, pageSize }] as const,
  infiniteTransactions: (pageSize: number = 20) =>
    [...financeKeys.all, "transactions", "infinite", { pageSize }] as const,
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

export const useInfiniteTransactions = (pageSize: number = 20) => {
  return useInfiniteQuery({
    queryKey: financeKeys.infiniteTransactions(pageSize),
    queryFn: async ({ pageParam = 1 }) => {
      const { data } = await api.get<PaginatedResponse<Transaction>>(
        `/finance/bank/transactions?page=${pageParam}&page_size=${pageSize}`,
      );
      return data;
    },
    initialPageParam: 1,
    getNextPageParam: (lastPage) => {
      // If there's a next page, return the next page number, otherwise return undefined
      return lastPage.pagination.has_next
        ? lastPage.pagination.page + 1
        : undefined;
    },
    getPreviousPageParam: (firstPage) => {
      // If there's a previous page, return the previous page number, otherwise return undefined
      return firstPage.pagination.has_prev
        ? firstPage.pagination.page - 1
        : undefined;
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

export const useAddOAuthBankAccount = () => {
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

export const useAddTokenBankAccount = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (bank_id: string) => {
      await api.post(`/finance/bank/add?bank_id=${bank_id}`);
    },
    onSuccess: () => {
      // Invalidate balances to refresh the data
      queryClient.invalidateQueries({ queryKey: financeKeys.balances() });

      // Invalidate both regular and paginated transaction queries
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
      const { data } = await api.put<Transaction>(
        `/finance/bank/${account_id}/transactions/${transaction_id}`,
        {
          description,
          subcategory_id,
          amount: parseFloat(amount.toString()),
        },
      );
      return data;
    },
    onSuccess: (updatedTransaction) => {
      // Update the transaction in the regular query cache
      queryClient.setQueryData(
        financeKeys.transactions(),
        (oldData: PaginatedResponse<Transaction> | undefined) => {
          if (!oldData) return oldData;

          return {
            ...oldData,
            items: oldData.items.map((transaction) =>
              transaction.id === updatedTransaction.id
                ? updatedTransaction
                : transaction,
            ),
          };
        },
      );

      // Update the transaction in the infinite query cache
      queryClient.setQueryData(
        financeKeys.infiniteTransactions(),
        (
          oldData:
            | { pages: PaginatedResponse<Transaction>[]; pageParams: unknown[] }
            | undefined,
        ) => {
          if (!oldData || !oldData.pages) return oldData;

          return {
            ...oldData,
            pages: oldData.pages.map(
              (page: PaginatedResponse<Transaction>) => ({
                ...page,
                items: page.items.map((transaction) =>
                  transaction.id === updatedTransaction.id
                    ? updatedTransaction
                    : transaction,
                ),
              }),
            ),
          };
        },
      );

      // Only invalidate categories to update the amounts
      queryClient.invalidateQueries({ queryKey: financeKeys.categories() });
    },
  });
};
