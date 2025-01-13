import { SubCategoryCard } from "~/components/SubCategoryCard";
import { Container, Title, Stack, Group } from "@mantine/core";
import { AddCategoryModal } from "~/components/modals/AddCategoryModal";
import { AddSubCategoryModal } from "~/components/modals/AddSubCategoryModal";

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
      <Group justify="apart" mb="md">
        <Title order={2}>Categories</Title>
        <AddCategoryModal />
      </Group>
      {categories.map((category) => (
        <div key={category.id}>
          <Group justify="apart" mb="md">
            <Title order={4}>{category.name}</Title>
            <AddSubCategoryModal categoryId={category.id} />
          </Group>
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
