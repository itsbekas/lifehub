import { SubCategoryCard } from "~/components/SubCategoryCard";
import { Divider, Group, Text, Stack, Space } from "@mantine/core";
import { AddSubCategoryModal } from "~/components/modals/AddSubCategoryModal";
import { useCategories, useTransactions } from "~/hooks/useFinanceQueries";
import { useContext } from "react";
import { TimeRangeContext } from "~/context/finance";

export function Categories() {
  const subcatBalances: Record<string, number> = {};

  const { timeRange } = useContext(TimeRangeContext);
  const transactions = useTransactions(timeRange)?.data || [];
  const categories = useCategories()?.data || [];

  // Calculate balances for each subcategory
  transactions.forEach((transaction) => {
    if (transaction.subcategory_id) {
      if (!subcatBalances[transaction.subcategory_id]) {
        subcatBalances[transaction.subcategory_id] = 0;
      }
      subcatBalances[transaction.subcategory_id] -= transaction.amount;
    }
  });

  return (
    <Stack p={4} gap="md">
      {categories.map((category) => {
        return (
          <Stack mb={4}>
            <Space h="md" />
            <Group justify="space-between" wrap="nowrap">
              <Text fw={600}>{category.name}</Text>
              <AddSubCategoryModal categoryId={category.id} />
            </Group>
            <Divider />
            <Stack>
              {category.subcategories.map((subcategory) => (
                <SubCategoryCard
                  key={subcategory.id}
                  name={subcategory.name}
                  budgeted={subcategory.budgeted}
                  spent={subcatBalances[subcategory.id] || 0}
                />
              ))}
            </Stack>
          </Stack>
        );
      })}
    </Stack>
  );
}
