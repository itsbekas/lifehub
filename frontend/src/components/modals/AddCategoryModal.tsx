import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, TextInput, Group } from "@mantine/core";
import { useCreateCategory } from "~/hooks/useFinanceQueries";

export function AddCategoryModal() {
  const [opened, { open, close }] = useDisclosure(false);
  const [categoryName, setCategoryName] = useState("");
  const createCategory = useCreateCategory();

  const handleSubmit = () => {
    if (!categoryName.trim()) {
      return;
    }

    // Use mutation hook instead of fetcher
    createCategory.mutate(categoryName, {
      onSuccess: () => {
        setCategoryName("");
        close();
      },
    });
  };

  return (
    <>
      <Modal opened={opened} onClose={close} title="Add Category" centered>
        <TextInput
          label="Category Name"
          placeholder="Enter category name"
          value={categoryName}
          onChange={(e) => setCategoryName(e.target.value)}
          required
          error={
            createCategory.error
              ? (createCategory.error as Error).message
              : undefined
          }
        />
        <Group align="right" mt="md">
          <Button variant="default" onClick={close}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} loading={createCategory.isPending}>
            Add
          </Button>
        </Group>
      </Modal>

      <Button onClick={open} size="compact-xs" variant="subtle">
        + Add Category
      </Button>
    </>
  );
}
