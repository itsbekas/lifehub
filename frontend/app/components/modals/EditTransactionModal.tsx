import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import {
  Modal,
  Button,
  Select,
  Group,
  ActionIcon,
  TextInput,
  NumberInput,
} from "@mantine/core";
import { useFetcher } from "react-router";
import { IconDots } from "@tabler/icons-react";

type SubCategory = {
  id: string;
  name: string;
};

type Transaction = {
  id: string;
  account_id: string;
  amount: number;
  date: string;
  description: string;
  counterparty: string;
  subcategory_id: string;
  user_description: string;
};

type EditTransactionModalProps = {
  subCategories: SubCategory[]; // List of available sub-categories
  transaction: Transaction; // ID of the transaction being edited
};

export function EditTransactionModal({
  subCategories,
  transaction,
}: EditTransactionModalProps) {
  const [opened, { open, close }] = useDisclosure(false);
  const [selectedSubCategory, setSelectedSubCategory] = useState<string | null>(
    subCategories.find(
      (subCategory) => subCategory.id === transaction.subcategory_id
    )?.id ?? null
  );
  const [description, setDescription] = useState<string>(
    transaction.description
  );
  const [amount, setAmount] = useState<number | string>(transaction.amount);
  const fetcher = useFetcher();

  const handleSubmit = () => {
    if (!selectedSubCategory) {
      return;
    }

    // Use fetcher.submit with JSON encoding
    fetcher.submit(
      {
        account_id: transaction.account_id,
        transaction_id: transaction.id,
        description,
        amount,
        subcategory_id: selectedSubCategory,
        action: "editTransaction",
      },
      { method: "post", encType: "application/json" }
    );

    // Close modal on success (optionally handle fetcher.state or errors)
    close();
  };

  return (
    <>
      <Modal opened={opened} onClose={close} title="Edit Transaction" centered>
        <TextInput
          label="Description"
          placeholder="Enter a description"
          value={description}
          onChange={(event) => setDescription(event.currentTarget.value)}
          required
          mb="sm"
        />
        <NumberInput
          label="Amount"
          placeholder="Enter amount"
          value={amount}
          onChange={setAmount}
          required
          decimalScale={2}
          mb="sm"
        />
        <Select
          label="Select Sub-Category"
          placeholder="Choose a sub-category"
          data={subCategories.map((subCategory) => ({
            value: subCategory.id,
            label: subCategory.name,
          }))}
          value={selectedSubCategory}
          onChange={setSelectedSubCategory}
          required
          mb="sm"
        />
        <Group align="right" mt="md">
          <Button variant="default" onClick={close}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} loading={fetcher.state !== "idle"}>
            Save
          </Button>
        </Group>
      </Modal>

      <ActionIcon onClick={open} size="compact-xs" variant="subtle">
        <IconDots size={16} stroke={1.5} />
      </ActionIcon>
    </>
  );
}
