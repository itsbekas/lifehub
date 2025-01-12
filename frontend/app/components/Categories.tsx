import React from "react";
import { SubCategoryCard } from "~/components/SubCategoryCard";
import { Container, Title, Stack } from "@mantine/core";

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
  return (
    <Container size="lg">
      <Title order={2}>Categories</Title>
      {categories.map((category) => (
        <div key={category.id}>
          <Title order={4} mt="lg" mb="md">
            {category.name}
          </Title>
          <Stack gap="md">
            {category.subcategories.map((subcategory) => (
              <SubCategoryCard
                key={subcategory.id}
                name={subcategory.name}
                budgeted={subcategory.budgeted}
                spent={subcategory.spent}
              />
            ))}
          </Stack>
        </div>
      ))}
    </Container>
  );
}
