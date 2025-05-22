import { Text } from "@mantine/core";
import { IconArrowDownRight } from "@tabler/icons-react";
import { StatCard } from "./StatCard";
import classes from "~/styles/FinanceDashboard.module.css";

interface ExpensesCardProps {
  expenses: number;
}

export function ExpensesCard({ expenses }: ExpensesCardProps) {
  return (
    <StatCard
      title="Expenses"
      value={`${expenses.toFixed(2)}€`}
      description={
        <Text size="sm" c="red">
          <IconArrowDownRight size={16} style={{ display: "inline" }} />{" "}
          Expenses this month
        </Text>
      }
      icon={<IconArrowDownRight size={24} />}
      iconClass={`${classes.statsIcon} ${classes.negative}`}
    />
  );
}
