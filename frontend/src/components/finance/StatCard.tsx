import { Card, Group, Text } from "@mantine/core";
import { ReactNode } from "react";
import classes from "~/styles/FinanceDashboard.module.css";

interface StatCardProps {
  title: string;
  value: string | number;
  description: ReactNode;
  icon: ReactNode;
  iconClass: string;
}

export function StatCard({
  title,
  value,
  description,
  icon,
  iconClass,
}: StatCardProps) {
  return (
    <Card className={classes.statsCard} withBorder>
      <Group justify="space-between" align="flex-start">
        <div>
          <Text size="xs" c="dimmed">
            {title}
          </Text>
          <Text size="xl" fw={700}>
            {value}
          </Text>
          {description}
        </div>
        <div className={iconClass}>{icon}</div>
      </Group>
    </Card>
  );
}
