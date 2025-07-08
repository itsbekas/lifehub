import { TransactionsTable } from "~/components/TransactionsTable";
import { BankBalances } from "~/components/BankBalances";
import { MonthlySummaryCard } from "~/components/finance/MonthlySummaryCard";
import { BudgetCategoriesCard } from "~/components/finance/BudgetCategoriesCard";
import { FinancialSummary } from "~/components/finance/FinancialSummary";
import { Grid, Title, Skeleton, Center, Text, Card } from "@mantine/core";
import { TimeRangeContext } from "~/context/finance";
import { createFileRoute } from "@tanstack/react-router";
import {
  useTransactions,
  useCategories,
  useBalances,
  useBanks,
} from "~/hooks/useFinanceQueries";
import type { SubCategory } from "~/hooks/useFinanceQueries";
import classes from "~/styles/FinanceDashboard.module.css";
import { useState } from "react";

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
  const date = new Date();
  const pad2 = (n: number) => n.toString().padStart(2, "0");
  const [timeRange, setTimeRange] = useState({
    startDate: `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-01`, // Start of the current month
    endDate: new Date().toISOString().split("T")[0],
  });

  const transactionsQuery = useTransactions(timeRange);
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
    <TimeRangeContext
      value={{
        timeRange,
        setTimeRange,
      }}
    >
      <div>
        <div className={classes.dashboardHeader}>
          <Title order={1}>Finance Dashboard</Title>
        </div>

        <Grid>
          {/* <Grid.Col span={4}>
            <FinancialSummary />
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
          </Grid.Col> */}
          <Grid.Col span={{ base: 12, md: 4, lg: 4 }}>
            <MonthlySummaryCard />
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 4, lg: 5 }}>
            <Card withBorder>
              <Title order={3} className={classes.sectionTitle}>
                Recent Transactions
              </Title>
              {transactionsQuery.isLoading || categoriesQuery.isLoading ? (
                <Skeleton height={600} />
              ) : (
                <TransactionsTable
                  transactions={transactionsQuery.data || []}
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
                />
              )}
            </Card>
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 4, lg: 3 }}>
            <BudgetCategoriesCard />
          </Grid.Col>
        </Grid>
      </div>
    </TimeRangeContext>
  );
}
