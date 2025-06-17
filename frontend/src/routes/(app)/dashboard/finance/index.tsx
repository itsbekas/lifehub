import { TransactionsTable } from "~/components/TransactionsTable";
import { BankBalances } from "~/components/BankBalances";
import { BudgetCategories } from "~/components/finance/BudgetCategories";
import { FinancialSummary } from "~/components/finance/FinancialSummary";
import { Grid, Title, Skeleton, Center, Text, Card } from "@mantine/core";
import { createFileRoute } from "@tanstack/react-router";
import {
  useCategories,
  useInfiniteTransactions,
  useBalances,
  useMonthlySummary,
  useBanks,
} from "~/hooks/useFinanceQueries";
import type { SubCategory } from "~/hooks/useFinanceQueries";
import classes from "~/styles/FinanceDashboard.module.css";

export const Route = createFileRoute("/(app)/dashboard/finance/")({
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
  const transactionsQuery = useInfiniteTransactions(20);
  const categoriesQuery = useCategories();
  const balancesQuery = useBalances();
  const banksQuery = useBanks();
  const monthlySummaryQuery = useMonthlySummary();

  // Flatten the transactions from all pages
  const allTransactions =
    transactionsQuery.data?.pages.flatMap((page) => page.items) || [];

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
  if (monthlySummaryQuery.isError) {
    return <QueryError error={monthlySummaryQuery.error as Error} />;
  }

  // Calculate total balance from bank balances
  const totalBalance =
    balancesQuery.data?.reduce(
      (total, account) => total + account.balance,
      0,
    ) || 0;

  // Get monthly summary data
  const monthlySummary = monthlySummaryQuery.data;
  const monthlyIncome = monthlySummary?.income || 0;
  const monthlyExpenses = monthlySummary?.expenses || 0;
  const monthlyBalance = monthlyIncome - monthlyExpenses;

  return (
    <div>
      <div className={classes.dashboardHeader}>
        <Title order={1}>Finance Dashboard</Title>
      </div>

      <Grid>
        <Grid.Col span={4}>
          <FinancialSummary
            totalBalance={totalBalance}
            monthlyBalance={monthlyBalance}
            income={monthlyIncome}
            expenses={monthlyExpenses}
          />

          <Card withBorder mb="md">
            <Title order={3} className={classes.sectionTitle}>
              Bank Accounts
            </Title>
            {balancesQuery.isLoading || banksQuery.isLoading ? (
              <Skeleton height={150} />
            ) : (
              <BankBalances
                balances={balancesQuery.data || []}
                banks={banksQuery.data || []}
              />
            )}
          </Card>
        </Grid.Col>
        <Grid.Col span={5}>
          <Card withBorder>
            <Title order={3} className={classes.sectionTitle}>
              Recent Transactions
            </Title>
            {transactionsQuery.isLoading || categoriesQuery.isLoading ? (
              <Skeleton height={600} />
            ) : (
              <TransactionsTable
                transactions={allTransactions}
                categories={
                  categoriesQuery.data
                    ? categoriesQuery.data.flatMap(
                        (c: { subcategories: SubCategory[] }) =>
                          c.subcategories,
                      )
                    : []
                }
                isInfinite={true}
                isLoading={transactionsQuery.isLoading}
                isFetchingNextPage={transactionsQuery.isFetchingNextPage}
                hasNextPage={transactionsQuery.hasNextPage}
                fetchNextPage={transactionsQuery.fetchNextPage}
              />
            )}
          </Card>
        </Grid.Col>
        <Grid.Col span={{ base: 12, md: 4, lg: 3 }}>
          <BudgetCategories />
        </Grid.Col>
      </Grid>
    </div>
  );
}
