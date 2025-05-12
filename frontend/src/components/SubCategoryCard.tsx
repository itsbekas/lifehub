import { Card, Progress, Text, Group, ActionIcon } from "@mantine/core";
import { IconDotsVertical } from "@tabler/icons-react";
import classes from "~/styles/SubCategoryCard.module.css";

type SubCategoryProps = {
  name: string;
  budgeted: number;
  spent: number;
};

export function SubCategoryCard({ name, budgeted, spent }: SubCategoryProps) {
  const percentage = budgeted > 0 ? (spent / budgeted) * 100 : 0;
  const available = budgeted - spent;

  // Determine progress color based on percentage
  const getProgressClass = () => {
    if (percentage < 70) return classes.progressLow;
    if (percentage < 90) return classes.progressMedium;
    return classes.progressHigh;
  };

  return (
    <Card withBorder padding="sm" className={classes.card}>
      <div className={classes.header}>
        <Text className={classes.name}>{name}</Text>
        <ActionIcon variant="subtle" color="gray" size="sm">
          <IconDotsVertical size={14} />
        </ActionIcon>
      </div>

      <div className={classes.amounts}>
        <div>
          <Text className={classes.spent}>{spent.toFixed(2)}€</Text>
          <Text className={classes.budgeted}>of {budgeted.toFixed(2)}€</Text>
        </div>
        <Text
          className={`${classes.available} ${available >= 0 ? classes.availablePositive : classes.availableNegative}`}
        >
          {available >= 0 ? "+" : ""}
          {available.toFixed(2)}€
        </Text>
      </div>

      <Progress
        value={percentage}
        size="sm"
        radius="xl"
        className={getProgressClass()}
      />
    </Card>
  );
}
