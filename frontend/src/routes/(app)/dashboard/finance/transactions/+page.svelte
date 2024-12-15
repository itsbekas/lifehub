<script lang="ts">
  import TransactionsTable from '@/components/finance/TransactionsTable.svelte';
  import AddBankDialog from '@/components/finance/modals/AddBankDialog.svelte';
  import type { BankBalance, BankTransaction, BudgetCategory } from '@/lib/types/finance';

  interface Props {
    data: {
      balances: BankBalance[];
      transactions: BankTransaction[];
      budgetCategories: BudgetCategory[];
    };
  }

  let { data }: Props = $props();
</script>

<section>
  <h1 class="mb-4 text-xl font-bold">Recent Transactions</h1>

  <!-- Bank Balances -->
  <div class="balances mb-6 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
    {#each data.balances as balance (balance.account_id)}
      <div class="rounded-lg border bg-gray-50 p-4">
        <h3 class="text-md font-medium">{balance.bank}</h3>
        <p>Balance: {balance.balance}€</p>
      </div>
    {/each}
    <AddBankDialog />
  </div>

  <!-- Transactions Table -->
  <TransactionsTable transactions={data.transactions} categories={data.budgetCategories} />
</section>
