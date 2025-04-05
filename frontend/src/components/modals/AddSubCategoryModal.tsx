import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, TextInput, Group, NumberInput } from "@mantine/core";
import { useCreateSubCategory } from "~/hooks/useFinanceQueries";

type AddSubCategoryModalProps = {
  categoryId: string; // The ID of the category to associate the sub-category with
};

export function AddSubCategoryModal({ categoryId }: AddSubCategoryModalProps) {
  const [opened, { open, close }] = useDisclosure(false);
  const [subCategoryName, setSubCategoryName] = useState("");
  const [amount, setAmount] = useState<string | number>("");
  const createSubCategory = useCreateSubCategory();

  const handleSubmit = () => {
    if (!subCategoryName.trim() || !amount) {
      return;
    }

    createSubCategory.mutate(
      {
        name: subCategoryName,
        amount: typeof amount === "string" ? parseFloat(amount) : amount,
        category_id: categoryId,
      },
      {
        onSuccess: () => {
          setSubCategoryName("");
          setAmount("");
          close();
        },
      },
    );
  };

  return (
    <>
      <Modal opened={opened} onClose={close} title="Add Sub-Category" centered>
        <TextInput
          label="Sub-Category Name"
          placeholder="Enter sub-category name"
          value={subCategoryName}
          onChange={(e) => setSubCategoryName(e.target.value)}
          required
          mb="sm"
        />

        <NumberInput
          label="Budgeted Amount"
          placeholder="Enter amount"
          value={amount}
          onChange={setAmount}
          required
          min={0}
          decimalScale={2}
          mb="sm"
        />

        <Group align="right" mt="md">
          <Button variant="default" onClick={close}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} loading={createSubCategory.isPending}>
            Add
          </Button>
        </Group>
      </Modal>

      <Button onClick={open} size="compact-xs" variant="subtle">
        + Add Sub-Category
      </Button>
    </>
  );
}
