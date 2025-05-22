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

  // Calculate total balance from bank balances
  const calculateTotalBalance = () => {
    if (!balancesQuery.data || balancesQuery.data.length === 0) return 0;

    return balancesQuery.data.reduce(
      (total, account) => total + account.balance,
      0,
    );
  };

  const totalBalance = calculateTotalBalance();

  // Get monthly summary data from account balances
  const getMonthlySummary = () => {
    if (!balancesQuery.data || balancesQuery.data.length === 0) {
      return { income: 0, expenses: 0, balance: 0 };
    }

    // Sum up monthly income and expenses from all accounts
    let totalIncome = 0;
    let totalExpenses = 0;

    balancesQuery.data.forEach((account) => {
      totalIncome += account.monthly_income;
      totalExpenses += account.monthly_expenses;
    });

    return {
      income: totalIncome,
      expenses: totalExpenses,
      balance: totalIncome - totalExpenses,
    };
  };

  const { income, expenses, balance: monthlyBalance } = getMonthlySummary();

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
        income={income}
        expenses={expenses}
      />

      <Grid>
        {/* Bank Balances */}
        <Grid.Col
          span={{ base: 12, md: 12, lg: 8 }}
          order={{ base: 2, md: 2, lg: 1 }}
        >
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

          {/* Transactions */}
          <Card withBorder>
            <Title order={3} className={classes.sectionTitle}>
              Recent Transactions
            </Title>
            {transactionsQuery.isLoading || categoriesQuery.isLoading ? (
              <Skeleton height={300} />
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
