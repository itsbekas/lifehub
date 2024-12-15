<script lang="ts">
  import * as Table from '@/components/ui/table';
  import * as Card from '@/components/ui/card';
  import type { BankTransaction, BudgetCategory } from '@/lib/types/finance';
  import EditTransactionDialog from './modals/EditTransactionDialog.svelte';

  export let transactions: BankTransaction[] = [];
  export let categories: BudgetCategory[] = [];

  /**
   * Helper function to find a subcategory name by its ID.
   * @param subcategoryId - The ID of the subcategory.
   * @returns The subcategory name, or undefined if not found.
   */
  function getSubcategoryById(subcategoryId: string | undefined): string | undefined {
    for (const category of categories) {
      for (const subcategory of category.subcategories) {
        if (subcategory.id === subcategoryId) {
          return subcategory.name;
        }
      }
    }
  }
</script>

<section>
  <Card.Root class="w-full">
    <Card.Header>
      <Card.Title>Recent Transactions</Card.Title>
      <Card.Description>A list of your recent transactions.</Card.Description>
    </Card.Header>
    <Card.Content>
      <Table.Root>
        <Table.Header>
          <Table.Row>
            <Table.Head class="w-auto">Description</Table.Head>
            <Table.Head>Sub-category</Table.Head>
            <Table.Head>Amount</Table.Head>
            <Table.Head class="text-right">Date</Table.Head>
            <Table.Head>Actions</Table.Head>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {#each transactions as transaction (transaction.id)}
            <Table.Row>
              <Table.Cell class="whitespace-normal break-words font-medium">
                {transaction.user_description
                  ? transaction.user_description
                  : `${transaction.description} (${transaction.counterparty})`}
              </Table.Cell>
              <Table.Cell>
                {getSubcategoryById(transaction.subcategory_id!) || 'Uncategorized'}
              </Table.Cell>
              <Table.Cell>{transaction.amount.toFixed(2)}€</Table.Cell>
              <Table.Cell class="text-right">
                {new Date(transaction.date).toLocaleDateString()}
              </Table.Cell>
              <Table.Cell>
                <EditTransactionDialog transaction={transaction} categories={categories} />
              </Table.Cell>
            </Table.Row>
          {/each}
        </Table.Body>
      </Table.Root>
    </Card.Content>
  </Card.Root>
</section>
