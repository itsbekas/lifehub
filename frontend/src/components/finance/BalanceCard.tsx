import { Text } from "@mantine/core";
import { IconCoin } from "@tabler/icons-react";
import { StatCard } from "./StatCard";
import classes from "~/styles/FinanceDashboard.module.css";

interface BalanceCardProps {
  totalBalance: number;
  monthlyBalance: number;
}

export function BalanceCard({
  totalBalance,
  monthlyBalance,
}: BalanceCardProps) {
  const isPositive = monthlyBalance >= 0;

  return (
    <StatCard
      title="Total Balance"
      value={`${totalBalance.toFixed(2)}€`}
      description={
        <Text size="sm" c={isPositive ? "green" : "red"}>
          {isPositive ? "Positive" : "Negative"} monthly trend
        </Text>
      }
      icon={<IconCoin size={24} />}
      iconClass={`${classes.statsIcon} ${isPositive ? classes.positive : classes.negative}`}
    />
  );
}
