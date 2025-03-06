import { fetchWithAuth } from "~/utils/apiClient";
import { TransactionsTable } from "~/components/TransactionsTable";
import { BankBalances } from "~/components/BankBalances";
import { Categories } from "~/components/Categories";
import { Grid, Container, Title, Stack } from "@mantine/core";
import type { Route } from "./+types/dashboard.finance";
import { redirect } from "react-router";

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

type BankBalance = {
  bank: string;
  account_id: string;
  balance: number;
};

type Bank = {
  id: string;
  name: string;
  logo: string;
};

export async function action({ request }: { request: Request }) {
  const contentType = request.headers.get("Content-Type");

  if (contentType === "application/json") {
    const body = await request.json();
    const {
      action,
      name,
      amount,
      description,
      category_id,
      bank_id,
      account_id,
      transaction_id,
      subcategory_id,
    } = body;

    switch (action) {
      case "createCategory": {
        if (!name || typeof name !== "string" || !name.trim()) {
          return new Response(
            JSON.stringify({ error: "Category name cannot be empty." }),
            {
              status: 400,
              headers: { "Content-Type": "application/json" },
            }
          );
        }

        try {
          const response = await fetchWithAuth(
            "/finance/budget/categories",
            {
              method: "POST",
              body: JSON.stringify({ name }),
            },
            request
          );

          if (!response.ok) {
            const errorData = await response.json();
            return new Response(
              JSON.stringify({
                error: errorData.message || "Failed to add category.",
              }),
              {
                status: response.status,
                headers: { "Content-Type": "application/json" },
              }
            );
          }

          const newCategory = await response.json();

          return new Response(
            JSON.stringify({ success: true, category: newCategory }),
            {
              status: 200,
              headers: { "Content-Type": "application/json" },
            }
          );
        } catch (err) {
          console.error(err);
          return new Response(
            JSON.stringify({ error: "An unexpected error occurred." }),
            {
              status: 500,
              headers: { "Content-Type": "application/json" },
            }
          );
        }
      }

      case "createSubCategory": {
        if (
          !name ||
          typeof name !== "string" ||
          !name.trim() ||
          !amount ||
          typeof category_id !== "string" ||
          !category_id.trim()
        ) {
          return new Response(
            JSON.stringify({
              error: "All fields (name, amount, category_id) are required.",
            }),
            {
              status: 400,
              headers: { "Content-Type": "application/json" },
            }
          );
        }

        try {
          const response = await fetchWithAuth(
            `/finance/budget/categories/${category_id}/subcategories`,
            {
              method: "POST",
              body: JSON.stringify({ name, amount: parseFloat(amount) }),
            },
            request
          );

          if (!response.ok) {
            const errorData = await response.json();
            return new Response(
              JSON.stringify({
                error: errorData.message || "Failed to add sub-category.",
              }),
              {
                status: response.status,
                headers: { "Content-Type": "application/json" },
              }
            );
          }

          const newSubCategory = await response.json();

          return new Response(
            JSON.stringify({ success: true, subCategory: newSubCategory }),
            {
              status: 200,
              headers: { "Content-Type": "application/json" },
            }
          );
        } catch (err) {
          console.error(err);
          return new Response(
            JSON.stringify({ error: "An unexpected error occurred." }),
            {
              status: 500,
              headers: { "Content-Type": "application/json" },
            }
          );
        }
      }

      case "addBankAccount": {
        if (!bank_id || typeof bank_id !== "string" || !bank_id.trim()) {
          return new Response(
            JSON.stringify({
              error: "Bank_id is required.",
            }),
            {
              status: 400,
              headers: { "Content-Type": "application/json" },
            }
          );
        }

        try {
          const response = await fetchWithAuth(
            `/finance/bank/login?bank_id=${bank_id}`,
            {},
            request
          );

          if (!response.ok) {
            const errorData = await response.json();
            return new Response(
              JSON.stringify({
                error: errorData.message || "Failed to add bank account.",
              }),
              {
                status: response.status,
                headers: { "Content-Type": "application/json" },
              }
            );
          }

          const login_url = await response.json();

          return redirect(login_url);
        } catch (err) {
          console.error(err);
          return new Response(
            JSON.stringify({ error: "An unexpected error occurred." }),
            {
              status: 500,
              headers: { "Content-Type": "application/json" },
            }
          );
        }
      }

      case "editTransaction": {
        if (!transaction_id || !subcategory_id) {
          return new Response(
            JSON.stringify({
              error: "Transaction ID and Sub-category ID are required.",
            }),
            {
              status: 400,
              headers: { "Content-Type": "application/json" },
            }
          );
        }

        try {
          const response = await fetchWithAuth(
            `/finance/bank/${account_id}/transactions/${transaction_id}`,
            {
              method: "PUT",
              body: JSON.stringify({
                description,
                subcategory_id,
                amount: parseFloat(amount),
              }),
            },
            request
          );

          if (!response.ok) {
            const errorData = await response.json();
            return new Response(
              JSON.stringify({
                error: errorData.message || "Failed to edit transaction.",
              }),
              {
                status: response.status,
                headers: { "Content-Type": "application/json" },
              }
            );
          }

          return new Response(JSON.stringify({ success: true }), {
            status: 200,
            headers: { "Content-Type": "application/json" },
          });
        } catch (err) {
          console.error(err);
          return new Response(
            JSON.stringify({ error: "An unexpected error occurred." }),
            {
              status: 500,
              headers: { "Content-Type": "application/json" },
            }
          );
        }
      }

      default:
        return new Response(JSON.stringify({ error: "Invalid action type." }), {
          status: 400,
          headers: { "Content-Type": "application/json" },
        });
    }
  }

  return new Response(JSON.stringify({ error: "Unsupported Content-Type." }), {
    status: 415,
    headers: { "Content-Type": "application/json" },
  });
}

export async function loader({ request }: Route.LoaderArgs) {
  // Fetch transactions
  const transactionsRes = await fetchWithAuth(
    "/finance/bank/transactions",
    undefined,
    request
  );
  if (!transactionsRes.ok) {
    throw new Error(
      `Failed to fetch transactions: ${transactionsRes.statusText}`
    );
  }
  const transactions: Transaction[] = await transactionsRes.json();

  // Fetch categories
  const categoriesRes = await fetchWithAuth(
    "/finance/budget/categories",
    undefined,
    request
  );
  if (!categoriesRes.ok) {
    throw new Error(`Failed to fetch categories: ${categoriesRes.statusText}`);
  }
  const categories: Category[] = await categoriesRes.json();

  // Fetch bank balances
  const balancesRes = await fetchWithAuth(
    "/finance/bank/balances",
    undefined,
    request
  );
  if (!balancesRes.ok) {
    throw new Error(`Failed to fetch bank balances: ${balancesRes.statusText}`);
  }
  const balances: BankBalance[] = await balancesRes.json();

  // Fetch banks
  const banksRes = await fetchWithAuth(
    "/finance/bank/banks",
    undefined,
    request
  );
  if (!banksRes.ok) {
    throw new Error(`Failed to fetch banks: ${banksRes.statusText}`);
  }
  const banks: Bank[] = await banksRes.json();

  // Return combined data
  return { transactions, categories, balances, banks };
}

export default function FinancePage({ loaderData }: Route.ComponentProps) {
  const { transactions, categories, balances, banks } = loaderData;

  return (
    <Container size="lg" mt="lg">
      <Title order={1} mb="lg">
        Finance Dashboard
      </Title>
      <Grid>
        {/* Categories Column */}
        <Grid.Col span={4}>
          <Categories categories={categories} />
        </Grid.Col>

        <Grid.Col span={8}>
          <Stack gap="md">
            <BankBalances balances={balances} banks={banks} />
            <TransactionsTable
              transactions={transactions}
              categories={categories.flatMap((c) => c.subcategories)}
            />
          </Stack>
        </Grid.Col>
      </Grid>
    </Container>
  );
}
