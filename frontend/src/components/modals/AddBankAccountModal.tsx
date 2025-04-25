import { useState, useEffect } from "react";
import { useDisclosure } from "@mantine/hooks";
import { Modal, Button, Group, Select, Text, Loader } from "@mantine/core";
import {
  useAddBankAccount,
  useBanksByCountry,
  useCountries,
} from "~/hooks/useFinanceQueries";

export function AddBankAccountModal() {
  const [opened, { open, close }] = useDisclosure(false);
  const [selectedBank, setSelectedBank] = useState<string | null>(null);
  const [selectedCountry, setSelectedCountry] = useState<string>("PT"); // Default to Portugal

  // Fetch countries
  const countriesQuery = useCountries();

  // Fetch banks by selected country
  const banksByCountryQuery = useBanksByCountry(selectedCountry);

  const addBankAccount = useAddBankAccount();

  // Reset selected bank when country changes
  useEffect(() => {
    setSelectedBank(null);
  }, [selectedCountry]);

  const handleSubmit = () => {
    if (!selectedBank || !selectedCountry) {
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
        {/* Country selector */}
        <Select
          label="Select Country"
          placeholder="Choose a country"
          data={
            countriesQuery.data
              ? countriesQuery.data.map((country) => ({
                  value: country.code,
                  label: country.name,
                }))
              : []
          }
          value={selectedCountry}
          onChange={(value) => setSelectedCountry(value || "PT")}
          required
          mb="md"
          disabled={countriesQuery.isLoading}
        />

        {/* Bank selector */}
        {banksByCountryQuery.isLoading ? (
          <Loader size="sm" />
        ) : banksByCountryQuery.data?.length === 0 ? (
          <Text c="dimmed" mb="sm">
            No banks available for this country
          </Text>
        ) : (
          <Select
            label="Select Bank"
            placeholder="Choose a bank"
            data={
              banksByCountryQuery.data
                ? banksByCountryQuery.data.map((bank) => ({
                    value: bank.id,
                    label: bank.name,
                  }))
                : []
            }
            value={selectedBank}
            onChange={setSelectedBank}
            required
            mb="sm"
          />
        )}

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
