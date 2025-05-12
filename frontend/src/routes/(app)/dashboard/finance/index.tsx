import { TransactionsTable } from "~/components/TransactionsTable";
import { BankBalances } from "~/components/BankBalances";
import { Categories } from "~/components/Categories";
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
import {
  IconArrowUpRight,
  IconArrowDownRight,
  IconCoin,
} from "@tabler/icons-react";
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

  // Calculate total income, expenses, and balance
  const calculateFinancialSummary = () => {
    if (!allTransactions.length) return { income: 0, expenses: 0, balance: 0 };

    let income = 0;
    let expenses = 0;

    allTransactions.forEach((transaction) => {
      if (transaction.amount > 0) {
        income += transaction.amount;
      } else {
        expenses += Math.abs(transaction.amount);
      }
    });

    return {
      income,
      expenses,
      balance: income - expenses,
    };
  };

  const { income, expenses, balance } = calculateFinancialSummary();

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
      <Grid mb="xl">
        <Grid.Col span={{ base: 12, md: 4 }}>
          <Card className={classes.statsCard} withBorder>
            <Group justify="space-between" align="flex-start">
              <div>
                <Text size="xs" c="dimmed">
                  Total Balance
                </Text>
                <Text size="xl" fw={700}>
                  {balance.toFixed(2)}€
                </Text>
                <Text size="sm" c={balance >= 0 ? "green" : "red"}>
                  {balance >= 0 ? "Positive" : "Negative"} balance
                </Text>
              </div>
              <div
                className={`${classes.statsIcon} ${balance >= 0 ? classes.positive : classes.negative}`}
              >
                <IconCoin size={24} />
              </div>
            </Group>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 4 }}>
          <Card className={classes.statsCard} withBorder>
            <Group justify="space-between" align="flex-start">
              <div>
                <Text size="xs" c="dimmed">
                  Income
                </Text>
                <Text size="xl" fw={700}>
                  {income.toFixed(2)}€
                </Text>
                <Text size="sm" c="green">
                  <IconArrowUpRight size={16} style={{ display: "inline" }} />{" "}
                  Income this month
                </Text>
              </div>
              <div className={`${classes.statsIcon} ${classes.positive}`}>
                <IconArrowUpRight size={24} />
              </div>
            </Group>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 4 }}>
          <Card className={classes.statsCard} withBorder>
            <Group justify="space-between" align="flex-start">
              <div>
                <Text size="xs" c="dimmed">
                  Expenses
                </Text>
                <Text size="xl" fw={700}>
                  {expenses.toFixed(2)}€
                </Text>
                <Text size="sm" c="red">
                  <IconArrowDownRight size={16} style={{ display: "inline" }} />{" "}
                  Expenses this month
                </Text>
              </div>
              <div className={`${classes.statsIcon} ${classes.negative}`}>
                <IconArrowDownRight size={24} />
              </div>
            </Group>
          </Card>
        </Grid.Col>
      </Grid>

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
