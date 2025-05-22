import {
  Card,
  Text,
  Group,
  SimpleGrid,
  Badge,
  ActionIcon,
} from "@mantine/core";
import { AddBankAccountModal } from "~/components/modals/AddBankAccountModal";
import { IconBuildingBank, IconDotsVertical } from "@tabler/icons-react";
import type { Bank } from "~/hooks/useFinanceQueries";
import classes from "~/styles/BankBalances.module.css";

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
  // Function to get a shortened account ID for display
  const getShortAccountId = (accountId: string) => {
    if (accountId.length <= 8) return accountId;
    return `${accountId.substring(0, 4)}...${accountId.substring(accountId.length - 4)}`;
  };

  return (
    <div>
      <Group justify="end" mb="md">
        <AddBankAccountModal />
      </Group>

      <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }} spacing="md">
        {balances.map((balance) => {
          const bank = banks.find((b) => b.id === balance.bank);
          const isPositive = balance.balance >= 0;

          return (
            <Card
              withBorder
              key={balance.account_id}
              padding="md"
              className={classes.bankCard}
            >
              <Group justify="space-between" mb="xs">
                <Group
                  gap="sm"
                  wrap="nowrap"
                  style={{ flex: 1, overflow: "hidden" }}
                >
                  <div className={classes.bankIcon}>
                    <IconBuildingBank size={20} />
                  </div>
                  <div style={{ minWidth: 0 }}>
                    <Text fw={600} size="md" truncate>
                      {bank?.name || balance.bank}
                    </Text>
                    <Group gap="xs">
                      <Badge
                        size="xs"
                        variant="light"
                        className={classes.accountBadge}
                      >
                        {getShortAccountId(balance.account_id)}
                      </Badge>
                    </Group>
                  </div>
                </Group>
                <ActionIcon
                  variant="subtle"
                  color="gray"
                  style={{ flexShrink: 0 }}
                >
                  <IconDotsVertical size={16} />
                </ActionIcon>
              </Group>

              <Text
                size="xl"
                fw={700}
                className={
                  isPositive ? classes.positiveBalance : classes.negativeBalance
                }
                mt="md"
              >
                {balance.balance.toFixed(2)}€
              </Text>
              <Text size="xs" c="dimmed">
                Current Balance
              </Text>
            </Card>
          );
        })}
      </SimpleGrid>
    </div>
  );
}
