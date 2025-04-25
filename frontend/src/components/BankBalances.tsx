import { Container, Title, Card, Text, Group } from "@mantine/core";
import { AddBankAccountModal } from "~/components/modals/AddBankAccountModal";
import type { Bank } from "~/hooks/useFinanceQueries";

type BankBalance = {
  bank: string;
  account_id: string;
  balance: number;
};

type BankBalancesProps = {
  balances: BankBalance[];
  banks: Bank[];
};

export function BankBalances({ balances, banks }: BankBalancesProps) {
  return (
    <Container size="lg" mt="lg">
      <Group justify="apart" mb="md">
        <Title order={2}>Bank Balances</Title>
        <AddBankAccountModal />
      </Group>
      <Group gap="md" align="left">
        {balances.map((balance) => {
          const bank = banks.find((b) => b.id === balance.bank);
          return (
            <Card
              withBorder
              radius="md"
              key={balance.account_id}
              padding="md"
              style={{ width: 200 }}
            >
              <Text fw={500} truncate>
                {bank?.name || balance.bank}
              </Text>
              <Text size="sm" c="dimmed" mb="xs" truncate>
                Account ID: {balance.account_id}
              </Text>
              <Text fw={700}>${balance.balance.toFixed(2)}</Text>
            </Card>
          );
        })}
      </Group>
    </Container>
  );
}
