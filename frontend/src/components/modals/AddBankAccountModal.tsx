import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, Group, Select } from "@mantine/core";
import { useFetcher } from "react-router";

type Bank = {
  id: string;
  name: string;
  logo: string; // Not used here but available for potential enhancements
};

type AddBankAccountModalProps = {
  banks: Bank[]; // List of available banks
};

export function AddBankAccountModal({ banks }: AddBankAccountModalProps) {
  const [opened, { open, close }] = useDisclosure(false);
  const [selectedBank, setSelectedBank] = useState<string | null>(null);
  const fetcher = useFetcher();

  const handleSubmit = () => {
    if (!selectedBank) {
      return;
    }

    // Use fetcher.submit with JSON encoding
    fetcher.submit(
      {
        bank_id: selectedBank,
        action: "addBankAccount",
      },
      { method: "post", encType: "application/json" }
    );
  };

  return (
    <>
      <Modal opened={opened} onClose={close} title="Add Bank Account" centered>
        <Select
          label="Select Bank"
          placeholder="Choose a bank"
          data={banks.map((bank) => ({
            value: bank.id,
            label: bank.name,
          }))}
          value={selectedBank}
          onChange={setSelectedBank}
          required
          mb="sm"
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
        + Add Bank Account
      </Button>
    </>
  );
}
