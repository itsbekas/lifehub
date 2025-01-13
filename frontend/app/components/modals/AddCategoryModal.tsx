import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, TextInput, Group } from "@mantine/core";
import { useFetcher } from "react-router";

export function AddCategoryModal() {
  const [opened, { open, close }] = useDisclosure(false);
  const [categoryName, setCategoryName] = useState("");
  const fetcher = useFetcher();

  const handleSubmit = () => {
    if (!categoryName.trim()) {
      return;
    }

    // Use fetcher.submit with JSON encoding
    fetcher.submit(
      { name: categoryName, action: "createCategory" },
      { method: "post", encType: "application/json" }
    );
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
          error={fetcher.data?.error}
        />
        <Group align="right" mt="md">
          <Button variant="default" onClick={close}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} loading={fetcher.state !== "idle"}>
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
