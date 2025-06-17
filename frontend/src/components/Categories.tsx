import { SubCategoryCard } from "~/components/SubCategoryCard";
import { Divider, Group, Text, Stack, Space } from "@mantine/core";
import { AddSubCategoryModal } from "~/components/modals/AddSubCategoryModal";
import type { CategoryMonthlySummary } from "~/hooks/useFinanceQueries";

type SubCategory = {
  id: string;
  name: string;
  category_id: string;
  category_name: string;
  budgeted: number;
};

type Category = {
  id: string;
  name: string;
  subcategories: SubCategory[];
};

type CategoriesProps = {
  categories: Category[];
  summary: CategoryMonthlySummary[];
};

export function Categories({ categories, summary }: CategoriesProps) {
  const subcatBalances: Record<string, number> = {};

  summary.forEach((item) => {
    subcatBalances[item.subcategory_id] = item.balance;
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
