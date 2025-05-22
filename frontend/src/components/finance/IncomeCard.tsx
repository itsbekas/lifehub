import { Text } from "@mantine/core";
import { IconArrowUpRight } from "@tabler/icons-react";
import { StatCard } from "./StatCard";
import classes from "~/styles/FinanceDashboard.module.css";

interface IncomeCardProps {
  income: number;
}

export function IncomeCard({ income }: IncomeCardProps) {
  return (
    <StatCard
      title="Income"
      value={`${income.toFixed(2)}€`}
      description={
        <Text size="sm" c="green">
          <IconArrowUpRight size={16} style={{ display: "inline" }} /> Income
          this month
        </Text>
      }
      icon={<IconArrowUpRight size={24} />}
      iconClass={`${classes.statsIcon} ${classes.positive}`}
    />
  );
}
