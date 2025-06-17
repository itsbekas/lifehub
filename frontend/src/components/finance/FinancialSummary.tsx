import { Grid } from "@mantine/core";
import { BalanceCard } from "./BalanceCard";
import { IncomeCard } from "./IncomeCard";
import { ExpensesCard } from "./ExpensesCard";
import { TimeRangeContext } from "~/context/finance";
import { useContext } from "react";
import { useBalances, useTransactions } from "~/hooks/useFinanceQueries";

export function FinancialSummary() {
  const { timeRange } = useContext(TimeRangeContext);
  const transactions = useTransactions(timeRange)?.data || [];
  const balances = useBalances()?.data || [];

  const totalBalance = balances.reduce(
    (acc, balance) => acc + balance.balance,
    0,
  );
  const monthlyBalance = transactions.reduce(
    (acc, transaction) => acc + transaction.amount,
    0,
  );
  const income = transactions
    .filter((transaction) => transaction.amount > 0)
    .reduce((acc, transaction) => acc + transaction.amount, 0);
  const expenses = transactions
    .filter((transaction) => transaction.amount < 0)
    .reduce((acc, transaction) => acc + transaction.amount, 0);

  return (
    <Grid mb="xl">
      <Grid.Col span={{ base: 12, md: 4 }}>
        <BalanceCard
          totalBalance={totalBalance}
          monthlyBalance={monthlyBalance}
        />
      </Grid.Col>

      <Grid.Col span={{ base: 12, md: 4 }}>
        <IncomeCard income={income} />
      </Grid.Col>

      <Grid.Col span={{ base: 12, md: 4 }}>
        <ExpensesCard expenses={expenses} />
      </Grid.Col>
    </Grid>
  );
}
