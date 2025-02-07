import { Container, Title, Card, Text, Group } from "@mantine/core";
import { AddBankAccountModal } from "~/components/modals/AddBankAccountModal";

type BankBalance = {
  bank: string;
  account_id: string;
  balance: number;
};

type Bank = {
  id: string;
  name: string;
  logo: string;
};

type BankBalancesProps = {
  balances: BankBalance[];
  banks: Bank[]; // List of available banks for the modal
};

export function BankBalances({ balances, banks }: BankBalancesProps) {
  return (
    <Container size="lg" mt="lg">
      <Group justify="apart" mb="md">
        <Title order={2}>Bank Balances</Title>
        <AddBankAccountModal banks={banks} />
      </Group>
      <Group gap="md" align="left">
        {balances.map((balance) => (
          <Card
            withBorder
            radius="md"
            key={balance.account_id}
            padding="md"
            style={{ width: 200 }} // Control card width
          >
            <Text fw={500} truncate>
              {balance.bank}
            </Text>
            <Text size="sm" c="dimmed" mb="xs" truncate>
              Account ID: {balance.account_id}
            </Text>
            <Text fw={700}>${balance.balance.toFixed(2)}</Text>
          </Card>
        ))}
      </Group>
    </Container>
  );
}
