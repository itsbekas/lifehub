import { useState, useEffect } from "react";
import { useDisclosure } from "@mantine/hooks";
import {
  Modal,
  Button,
  Group,
  Select,
  Text,
  Loader,
  Alert,
} from "@mantine/core";
import { IconInfoCircle } from "@tabler/icons-react";
import { Link } from "@tanstack/react-router";
import {
  useAddBankAccount,
  useBanksByCountry,
  useCountries,
} from "~/hooks/useFinanceQueries";
import { useProviders } from "~/hooks/useUserProviderQueries";
import { useAddTokenBankAccount } from "~/hooks/useFinanceQueries";

export function AddBankAccountModal() {
  const [opened, { open, close }] = useDisclosure(false);
  const [selectedBank, setSelectedBank] = useState<string | null>(null);
  const [selectedCountry, setSelectedCountry] = useState<string>("PT"); // Default to Portugal

  // Fetch countries
  const countriesQuery = useCountries();

  // Fetch banks by selected country
  const banksByCountryQuery = useBanksByCountry(selectedCountry);

  const providersQuery = useProviders();
  const addOAuthBankAccount = useAddBankAccount();
  const addTokenBankAccount = useAddTokenBankAccount();

  // Reset selected bank when country changes
  useEffect(() => {
    setSelectedBank(null);
  }, [selectedCountry]);

  const selectedBankData = banksByCountryQuery.data?.find(
    (bank) => bank.id === selectedBank,
  );

  const hasRequiredProvider =
    selectedBankData?.type === "oauth" ||
    (selectedBankData?.type === "token" &&
      providersQuery.data?.some((p) => p.id === selectedBankData.id));

  const handleSubmit = () => {
    if (!selectedBank || !selectedCountry || !hasRequiredProvider) {
      return;
    }

    if (selectedBankData?.type === "oauth") {
      addOAuthBankAccount.mutate(selectedBank, {
        onSuccess: (loginUrl) => {
          window.location.href = loginUrl;
        },
      });
    } else if (selectedBankData?.type === "token") {
      addTokenBankAccount.mutate(selectedBank, {
        onSuccess: () => {
          close();
        },
      });
    }
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

        {selectedBankData?.type === "token" && !hasRequiredProvider && (
          <Alert
            icon={<IconInfoCircle size="1rem" />}
            title="Provider Required"
            color="blue"
            mb="md"
          >
            <Text mb="sm">
              To connect this institution, you first need to set up your{" "}
              {selectedBankData.name} provider.
            </Text>
            <Button
              component={Link}
              to="/settings"
              onClick={() => close()}
              variant="light"
              color="blue"
              size="xs"
              fullWidth
            >
              Go to Provider Settings
            </Button>
          </Alert>
        )}

        <Group align="right" mt="md">
          <Button variant="default" onClick={close}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            loading={
              addOAuthBankAccount.isPending || addTokenBankAccount.isPending
            }
            disabled={!hasRequiredProvider}
          >
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
