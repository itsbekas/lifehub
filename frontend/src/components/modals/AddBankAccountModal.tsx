import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, Group, Select } from "@mantine/core";
import { useAddBankAccount } from "~/hooks/useFinanceQueries";

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
  const addBankAccount = useAddBankAccount();

  const handleSubmit = () => {
    if (!selectedBank) {
      return;
    }

    addBankAccount.mutate(selectedBank, {
      onSuccess: (loginUrl) => {
        window.location.href = loginUrl;
      },
    });
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
          <Button onClick={handleSubmit} loading={addBankAccount.isPending}>
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
