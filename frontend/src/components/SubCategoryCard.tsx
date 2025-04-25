import { Card, Progress, Text } from "@mantine/core";

type SubCategoryProps = {
  name: string;
  budgeted: number;
  spent: number;
};

export function SubCategoryCard({ name, budgeted, spent }: SubCategoryProps) {
  const percentage = budgeted > 0 ? (spent / budgeted) * 100 : 0;

  return (
    <Card
      withBorder
      radius="sm"
      padding="md"
      style={{ width: "100%", maxWidth: 300 }}
    >
      <Text fz="xs" tt="uppercase" fw={700} c="dimmed">
        {name}
      </Text>
      <Text fz="sm" fw={500} mt="xs">
        {spent.toFixed(2)}€ / {budgeted.toFixed(2)}€
      </Text>
      <Progress value={percentage} mt="sm" size="sm" radius="lg" />
    </Card>
  );
}
