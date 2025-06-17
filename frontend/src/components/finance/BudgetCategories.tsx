import { Card, Group, Title, Badge, Skeleton } from "@mantine/core";
import { useCategories } from "~/hooks/useFinanceQueries";
import { Categories } from "~/components/Categories";
import classes from "~/styles/FinanceDashboard.module.css";

export function BudgetCategories() {
  const categoriesQuery = useCategories();

  const calculateBudgetProgress = () => {
    if (!categoriesQuery.data) return 0;

    let totalBudgeted = 0;
    let totalSpent = 0;

    categoriesQuery.data.forEach((category) => {
      category.subcategories.forEach((subcategory) => {
        totalBudgeted += subcategory.budgeted;
        totalSpent += subcategory.spent;
      });
    });

    return totalBudgeted > 0 ? (totalSpent / totalBudgeted) * 100 : 0;
  };
  const budgetProgress = calculateBudgetProgress();

  return (
    <Card withBorder h="100%">
      <Group justify="space-between" mb="md">
        <Title order={3} className={classes.sectionTitle}>
          Budget Categories
        </Title>
        {/* <AddCategoryModal /> */}
        <Badge
          size="lg"
          color={
            budgetProgress > 90
              ? "red"
              : budgetProgress > 75
                ? "yellow"
                : "green"
          }
        >
          {Math.round(budgetProgress)}% Used
        </Badge>
      </Group>
      {categoriesQuery.isLoading ? (
        <Skeleton height={400} />
      ) : (
        <Categories categories={categoriesQuery.data || []} summary={[]} />
      )}
    </Card>
  );
}
