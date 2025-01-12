import { fetchWithAuth } from "~/utils/apiClient";
import { TransactionsTable } from "~/components/TransactionsTable";
import { Categories } from "~/components/Categories";
import { Grid, Container, Title } from "@mantine/core";
import type { Route } from "./+types/dashboard.finance";

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

export async function loader({ request }: Route.LoaderArgs) {
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

  const categoriesRes = await fetchWithAuth(
    "/finance/budget/categories",
    undefined,
    request
  );
  if (!categoriesRes.ok) {
    throw new Error(`Failed to fetch categories: ${categoriesRes.statusText}`);
  }
  const categories: Category[] = await categoriesRes.json();

  return { transactions, categories };
}

export default function FinancePage({ loaderData }: Route.ComponentProps) {
  const { transactions, categories } = loaderData;

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

        {/* Transactions Column */}
        <Grid.Col span={8}>
          <TransactionsTable
            transactions={transactions}
            categories={categories.flatMap((c) => c.subcategories)}
          />
        </Grid.Col>
      </Grid>
    </Container>
  );
}
