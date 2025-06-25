import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, Stack, Title, Text, Group, Divider } from "@mantine/core";
import { useContext } from "react";
import { TimeRangeContext } from "~/context/finance";
import { useBalances, useTransactions } from "~/hooks/useFinanceQueries";
import { IconArrowUpRight, IconArrowDownRight } from "@tabler/icons-react";

export const MonthlySummaryCard = () => {
  const { timeRange } = useContext(TimeRangeContext);
  const transactions = useTransactions(timeRange)?.data || [];
  const balances = useBalances()?.data || [];

  const totalBalance =
    balances.reduce((acc, balance) => acc + balance.balance, 0) - 4000;

  const expenses = transactions
    .filter((transaction) => transaction.amount < 0)
    .reduce((acc, transaction) => acc + transaction.amount, 0);

  const income = transactions
    .filter((transaction) => transaction.amount > 0)
    .reduce((acc, transaction) => acc + transaction.amount, 0);

  const netChange = income + expenses;
  const changePercentage =
    totalBalance !== 0 ? (netChange / (totalBalance + netChange)) * 100 : 0;

  const getBalanceEvolutionData = (currentTotalBalance, monthTransactions) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    firstDayOfMonth.setHours(0, 0, 0, 0);

    const dailyNetChanges = monthTransactions.reduce((acc, tx) => {
      const txDate = new Date(tx.date);
      txDate.setHours(0, 0, 0, 0);
      const dateKey = txDate.toISOString().split("T")[0];
      acc[dateKey] = (acc[dateKey] || 0) + tx.amount;
      return acc;
    }, {});

    const chartData = [];
    let runningBalance = currentTotalBalance;

    for (
      let d = new Date(today);
      d >= firstDayOfMonth;
      d.setDate(d.getDate() - 1)
    ) {
      const dateKey = d.toISOString().split("T")[0];
      const netChangeForDay = dailyNetChanges[dateKey] || 0;

      if (d.toDateString() === today.toDateString()) {
        chartData.unshift({
          date: d.toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "short",
          }),
          balance: runningBalance,
        });
      } else {
        runningBalance -= netChangeForDay;
        chartData.unshift({
          date: d.toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "short",
          }),
          balance: runningBalance,
        });
      }
    }

    if (chartData.length === 0 && currentTotalBalance !== undefined) {
      chartData.push({
        date: today.toLocaleDateString("en-GB", {
          day: "2-digit",
          month: "short",
        }),
        balance: currentTotalBalance,
      });
    }

    return chartData;
  };

  const balanceEvolutionData = getBalanceEvolutionData(
    totalBalance,
    transactions,
  );

  const formatBalance = (value: number, name: string, props: any) => {
    return [value.toFixed(2) + "€"];
  };

  return (
    <Card withBorder>
      <Stack>
        <Title order={3}>This Month</Title>
        <Group>
          <Text c="dimmed">Total Balance</Text>
          <Group>
            <Text fw={700} c="black">
              {totalBalance.toFixed(2)}€
            </Text>
            <Text c="dimmed" span>
              {netChange >= 0 ? "+" : ""}
            </Text>
            <Text
              c={netChange > 0 ? "green" : netChange < 0 ? "red" : "dimmed"}
            >
              {netChange.toFixed(2)}€ ({changePercentage.toFixed(2)}%)
            </Text>
          </Group>
        </Group>
        <Group>
          <Text c="dimmed">Total Income</Text>
          <Text fw={700} c="green.6">
            {income.toFixed(2)}€
          </Text>
        </Group>
        <Group>
          <Text c="dimmed">Total Expenses</Text>
          <Text fw={700} c="red.6">
            {Math.abs(expenses).toFixed(2)}€
          </Text>
        </Group>
        <Divider my="sm" />
        <Text c="dimmed">Balance Evolution</Text>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart
            data={balanceEvolutionData}
            margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
          >
            <XAxis dataKey="date" />
            <YAxis type="number" domain={["auto", "auto"]} />
            <Tooltip formatter={formatBalance} />
            <Line
              type="basis"
              dataKey="balance"
              stroke={netChange >= 0 ? "green" : "red"}
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </Stack>
    </Card>
  );
};
