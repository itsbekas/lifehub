import { SubCategoryCard } from "~/components/SubCategoryCard";
import { Button, Group, Text, ActionIcon, Accordion } from "@mantine/core";
import { AddCategoryModal } from "~/components/modals/AddCategoryModal";
import { AddSubCategoryModal } from "~/components/modals/AddSubCategoryModal";
import { IconPlus, IconFolder } from "@tabler/icons-react";
import classes from "~/styles/Categories.module.css";

type SubCategory = {
  id: string;
  name: string;
  category_id: string;
  category_name: string;
  budgeted: number;
  spent: number;
  available: number;
};

type Category = {
  id: string;
  name: string;
  subcategories: SubCategory[];
};

type CategoriesProps = {
  categories: Category[];
};

export function Categories({ categories }: CategoriesProps) {
  // Calculate total budgeted and spent for each category
  const getCategoryTotals = (subcategories: SubCategory[]) => {
    return subcategories.reduce(
      (acc, subcategory) => {
        acc.budgeted += subcategory.budgeted;
        acc.spent += subcategory.spent;
        return acc;
      },
      { budgeted: 0, spent: 0 },
    );
  };

  return (
    <div>
      <Group justify="end" mb="md">
        <AddCategoryModal />
      </Group>

      <Accordion variant="separated">
        {categories.map((category) => {
          const { budgeted, spent } = getCategoryTotals(category.subcategories);
          const percentage =
            budgeted > 0 ? Math.round((spent / budgeted) * 100) : 0;

          return (
            <Accordion.Item key={category.id} value={category.id}>
              <Accordion.Control icon={<IconFolder size={20} />}>
                <Group justify="space-between" wrap="nowrap">
                  <Text fw={600}>{category.name}</Text>
                  <Group gap="xs">
                    <Text size="sm" c="dimmed">
                      {spent.toFixed(2)}€ / {budgeted.toFixed(2)}€
                    </Text>
                    <Text
                      size="sm"
                      fw={500}
                      c={
                        percentage > 90
                          ? "red"
                          : percentage > 75
                            ? "yellow"
                            : "green"
                      }
                    >
                      {percentage}%
                    </Text>
                  </Group>
                </Group>
              </Accordion.Control>

              <Accordion.Panel>
                <Group justify="end" mb="sm">
                  <AddSubCategoryModal categoryId={category.id} />
                </Group>

                <div className={classes.subcategoryGrid}>
                  {category.subcategories.map((subcategory) => (
                    <SubCategoryCard
                      key={subcategory.id}
                      name={subcategory.name}
                      budgeted={subcategory.budgeted}
                      spent={subcategory.spent}
                    />
                  ))}
                </div>
              </Accordion.Panel>
            </Accordion.Item>
          );
        })}
      </Accordion>
    </div>
  );
}
