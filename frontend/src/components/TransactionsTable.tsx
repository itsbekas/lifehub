import { useState } from "react";
import cx from "clsx";
import {
  ScrollArea,
  Table,
  Text,
  Group,
  TextInput,
  Select,
} from "@mantine/core";
import { IconSearch, IconFilter } from "@tabler/icons-react";
import classes from "~/styles/TransactionsTable.module.css";
import { EditTransactionModal } from "~/components/modals/EditTransactionModal";

type SubCategory = {
  id: string;
  name: string;
  category_id: string;
  category_name: string;
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

type TransactionsTableProps = {
  transactions: Transaction[];
  categories: SubCategory[];
  isLoading?: boolean;
  isFetchingNextPage?: boolean;
  hasNextPage?: boolean;
  fetchNextPage?: () => void;
  isInfinite?: boolean;
};

export function TransactionsTable({
  transactions,
  categories,
}: TransactionsTableProps) {
  const [scrolled, setScrolled] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<string | null>(null);

  // Sort transactions from most recent to oldest
  const sortedTransactions = [...transactions].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
  );

  // Filter transactions based on search term and category filter
  const filteredTransactions = sortedTransactions.filter((transaction) => {
    const matchesSearch =
      searchTerm === "" ||
      transaction.description
        .toLowerCase()
        .includes(searchTerm.toLowerCase()) ||
      transaction.counterparty.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesCategory =
      categoryFilter === null || transaction.subcategory_id === categoryFilter;

    return matchesSearch && matchesCategory;
  });

  // Custom date formatter for DD-MM-YYYY
  const formatDate = (date: string) => {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();
    return `${day}-${month}-${year}`;
  };

  // Prepare category options for the filter dropdown
  const categoryOptions = categories.map((cat) => ({
    value: cat.id,
    label: `${cat.category_name}: ${cat.name}`,
  }));

  const rows = filteredTransactions.map((transaction) => {
    // Find the sub-category name using subcategory_id
    const subcategory = categories.find(
      (cat) => cat.id === transaction.subcategory_id,
    );
    const categoryName = subcategory?.name || "";
    const isPositive = transaction.amount >= 0;

    return (
      <Table.Tr key={transaction.id} className={classes.tableRow}>
        <Table.Td className={classes.dateCell}>
          {formatDate(transaction.date)}
        </Table.Td>
        <Table.Td>
          <Text fw={500}>{transaction.description}</Text>
          {transaction.user_description && (
            <Text size="xs" c="dimmed">
              {transaction.user_description}
            </Text>
          )}
        </Table.Td>
        <Table.Td>
          <span className={classes.categoryBadge}>{categoryName}</span>
        </Table.Td>
        <Table.Td
          className={`${classes.amountCell} ${isPositive ? classes.positive : classes.negative}`}
        >
          {isPositive ? "+" : ""}
          {transaction.amount.toFixed(2)}€
        </Table.Td>
        <Table.Td>
          <EditTransactionModal
            subCategories={categories}
            transaction={transaction}
          />
        </Table.Td>
      </Table.Tr>
    );
  });

  return (
    <div>
      <Group mb="md">
        <TextInput
          placeholder="Search transactions..."
          leftSection={<IconSearch size={16} />}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.currentTarget.value)}
          style={{ flex: 1 }}
        />
        <Select
          placeholder="Filter by category"
          data={categoryOptions}
          value={categoryFilter}
          onChange={setCategoryFilter}
          leftSection={<IconFilter size={16} />}
          clearable
          style={{ width: 250 }}
        />
      </Group>

      <ScrollArea.Autosize
        h={400}
        onScrollPositionChange={({ y }) => setScrolled(y !== 0)}
      >
        <Table className={classes.table}>
          <Table.Thead
            className={cx(classes.header, { [classes.scrolled]: scrolled })}
          >
            <Table.Tr>
              <Table.Th>Date</Table.Th>
              <Table.Th>Description</Table.Th>
              <Table.Th>Category</Table.Th>
              <Table.Th style={{ textAlign: "right" }}>Amount</Table.Th>
              <Table.Th />
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </ScrollArea.Autosize>

      <Group justify="space-between" mt="xs">
        <Text size="sm" c="dimmed">
          Showing {transactions.length} transactions
        </Text>
      </Group>
    </div>
  );
}
