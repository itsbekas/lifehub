import { Group, Progress, Text, Stack } from "@mantine/core";
import classes from "~/styles/SubCategoryCard.module.css";

type SubCategoryProps = {
  name: string;
  budgeted: number;
  spent: number;
};

export function SubCategoryCard({ name, budgeted, spent }: SubCategoryProps) {
  const percentage = budgeted > 0 ? (spent / budgeted) * 100 : 0;

  // Determine progress color based on percentage
  const getProgressClass = () => {
    if (percentage < 70) return classes.progressLow;
    if (percentage < 90) return classes.progressMedium;
    return classes.progressHigh;
  };

  return (
    <Stack gap={0}>
      <Group justify="space-between">
        <Text fw={600}>{name}</Text>
        <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
          <Text className={classes.spent}>{spent.toFixed(2)}€</Text>
          <Text className={classes.budgeted}>of {budgeted.toFixed(2)}€</Text>
        </div>
      </Group>

      <Progress
        value={percentage}
        size="sm"
        radius="xl"
        className={getProgressClass()}
      />
    </Stack>
  );
}
