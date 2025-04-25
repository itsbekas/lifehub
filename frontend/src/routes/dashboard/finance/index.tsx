import { TransactionsTable } from "~/components/TransactionsTable";
import { BankBalances } from "~/components/BankBalances";
import { Categories } from "~/components/Categories";
import {
  Grid,
  Container,
  Title,
  Stack,
  Skeleton,
  Center,
  Text,
} from "@mantine/core";
import { createFileRoute } from "@tanstack/react-router";
import {
  useCategories,
  useTransactions,
  useBalances,
  useBanks,
} from "~/hooks/useFinanceQueries";
import type { SubCategory } from "~/hooks/useFinanceQueries";

export const Route = createFileRoute("/dashboard/finance/")({
  component: FinancePage,
});

function QueryError({ error }: { error: Error }) {
  return (
    <Center>
      <Text c="red">{error.message}</Text>
    </Center>
  );
}

export default function FinancePage() {
  const transactionsQuery = useTransactions();
  const categoriesQuery = useCategories();
  const balancesQuery = useBalances();
  const banksQuery = useBanks();

  // Check for errors
  if (transactionsQuery.isError) {
    return <QueryError error={transactionsQuery.error as Error} />;
  }
  if (categoriesQuery.isError) {
    return <QueryError error={categoriesQuery.error as Error} />;
  }
  if (balancesQuery.isError) {
    return <QueryError error={balancesQuery.error as Error} />;
  }
  if (banksQuery.isError) {
    return <QueryError error={banksQuery.error as Error} />;
  }

  return (
    <Container size="lg" mt="lg">
      <Title order={1} mb="lg">
        Finance Dashboard
      </Title>

      <Grid>
        {/* Categories Column */}
        <Grid.Col span={4}>
          {categoriesQuery.isLoading ? (
            <Skeleton height={400} />
          ) : (
            <Categories categories={categoriesQuery.data || []} />
          )}
        </Grid.Col>

        <Grid.Col span={8}>
          <Stack gap="md">
            {balancesQuery.isLoading || banksQuery.isLoading ? (
              <Skeleton height={150} />
            ) : (
              <BankBalances
                balances={balancesQuery.data || []}
                banks={banksQuery.data || []}
              />
            )}

            {transactionsQuery.isLoading || categoriesQuery.isLoading ? (
              <Skeleton height={300} />
            ) : (
              <TransactionsTable
                transactions={transactionsQuery.data?.items || []}
                categories={
                  categoriesQuery.data
                    ? categoriesQuery.data.flatMap(
                        (c: { subcategories: SubCategory[] }) =>
                          c.subcategories,
                      )
                    : []
                }
              />
            )}
          </Stack>
        </Grid.Col>
      </Grid>
    </Container>
  );
}
