import { Grid } from "@mantine/core";
import { BalanceCard } from "./BalanceCard";
import { IncomeCard } from "./IncomeCard";
import { ExpensesCard } from "./ExpensesCard";

interface FinancialSummaryProps {
  totalBalance: number;
  monthlyBalance: number;
  income: number;
  expenses: number;
}

export function FinancialSummary({
  totalBalance,
  monthlyBalance,
  income,
  expenses,
}: FinancialSummaryProps) {
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
