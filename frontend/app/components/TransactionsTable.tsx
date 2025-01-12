import React from "react";
import { ScrollArea, Table } from "@mantine/core";

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
};

export function TransactionsTable({
  transactions,
  categories,
}: TransactionsTableProps) {
  // Sort transactions from most recent to oldest
  const sortedTransactions = [...transactions].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  // Custom date formatter for DD-MM-YYYY
  const formatDate = (date: string) => {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();
    return `${day}-${month}-${year}`;
  };

  const rows = sortedTransactions.map((transaction) => {
    // Find the sub-category name using subcategory_id
    const subcategory = categories.find(
      (cat) => cat.id === transaction.subcategory_id
    );
    const categoryName = subcategory?.name || "Uncategorized";

    return (
      <Table.Tr key={transaction.id}>
        <Table.Td>{formatDate(transaction.date)}</Table.Td>
        <Table.Td>{transaction.description}</Table.Td>
        <Table.Td>{categoryName}</Table.Td>
        <Table.Td>{transaction.amount.toFixed(2)}€</Table.Td>
      </Table.Tr>
    );
  });

  return (
    <ScrollArea h={300}>
      <Table miw={700}>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Date</Table.Th>
            <Table.Th>Description</Table.Th>
            <Table.Th>Category</Table.Th>
            <Table.Th>Amount</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </ScrollArea>
  );
}
