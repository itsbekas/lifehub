import { TransactionsTable } from "~/components/TransactionsTable";
import { BankBalances } from "~/components/BankBalances";
import { Categories } from "~/components/Categories";
import { FinancialSummary } from "~/components/finance/FinancialSummary";
import {
  Grid,
  Title,
  Skeleton,
  Center,
  Text,
  Card,
  Group,
  Badge,
} from "@mantine/core";
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

  // Calculate budget progress
  const calculateBudgetProgress = () => {
    if (!categoriesQuery.data) return 0;

    let totalBudgeted = 0;
    let totalSpent = 0;

    categoriesQuery.data.forEach((category) => {
      category.subcategories.forEach((subcategory) => {
        totalBudgeted += subcategory.budgeted;
        totalSpent += subcategory.spent;
      });
    });

    return totalBudgeted > 0 ? (totalSpent / totalBudgeted) * 100 : 0;
  };

  const budgetProgress = calculateBudgetProgress();

  return (
    <div>
      <div className={classes.dashboardHeader}>
        <Title order={1}>Finance Dashboard</Title>
      </div>

      {/* Financial Summary Cards */}
      <FinancialSummary
        totalBalance={totalBalance}
        monthlyBalance={monthlyBalance}
        income={monthlyIncome}
        expenses={monthlyExpenses}
      />

      {/* Bank Balances - Stacked vertically above everything */}
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

      <Grid>
        {/* Transactions - Now takes more space */}
        <Grid.Col
          span={{ base: 12, md: 12, lg: 8 }}
          order={{ base: 2, md: 2, lg: 1 }}
        >
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

        {/* Categories */}
        <Grid.Col
          span={{ base: 12, md: 12, lg: 4 }}
          order={{ base: 1, md: 1, lg: 2 }}
        >
          <Card withBorder h="100%">
            <Group justify="space-between" mb="md">
              <Title order={3} className={classes.sectionTitle}>
                Budget Categories
              </Title>
              <Badge
                size="lg"
                color={
                  budgetProgress > 90
                    ? "red"
                    : budgetProgress > 75
                      ? "yellow"
                      : "green"
                }
              >
                {Math.round(budgetProgress)}% Used
              </Badge>
            </Group>

            {categoriesQuery.isLoading ? (
              <Skeleton height={400} />
            ) : (
              <Categories categories={categoriesQuery.data || []} />
            )}
          </Card>
        </Grid.Col>
      </Grid>
    </div>
  );
}
