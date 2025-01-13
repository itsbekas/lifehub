import { Container, Title, Card, Text, Group } from "@mantine/core";

type BankBalance = {
  bank: string;
  account_id: string;
  balance: number;
};

type BankBalancesProps = {
  balances: BankBalance[];
};

export function BankBalances({ balances }: BankBalancesProps) {
  return (
    <Container size="lg" mt="lg">
      <Title order={2} mb="md">
        Bank Balances
      </Title>
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
