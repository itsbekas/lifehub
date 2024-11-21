<script lang="ts">
    import type { BankBalance, BankTransaction } from "@/lib/types/finance";
    import * as Table from "@/components/ui/table";

    // Define the Props interface as requested
    interface Props {
        data: { balances: BankBalance[], transactions: BankTransaction[], banks: string[] };
    }

    // Use the $props rune to destructure the props based on the defined interface
    let { data }: Props = $props();

    // Reactive state for managing modal visibility using $state
    let addBankModalVisible = $state(false);

    function openAddBankModal() {
        addBankModalVisible = true;
    }

    function closeAddBankModal() {
        addBankModalVisible = false;
    }

    function addBank() {
        // Logic to add bank goes here
        closeAddBankModal();
    }

    // Custom wrapper function for event.preventDefault
    function preventDefault(fn: (event: Event) => void) {
        return function (event: Event) {
            event.preventDefault();
            fn.call(this, event);
        };
    }
</script>

<div class="balances-section mb-6">
    <h2 class="text-xl font-bold mb-4">Bank Balances</h2>
    <div class="balances flex flex-col gap-4">
        {#each data.balances as balance (balance.bank)}
            <div class="card border border-gray-300 rounded-lg p-4 w-48 shadow-md">
                <h3 class="text-lg font-semibold mb-2">{balance.bank}</h3>
                <p class="text-gray-700">Balance: {balance.balance}</p>
            </div>
        {/each}
    </div>
</div>

<div class="transactions-section">
    <h2 class="text-xl font-bold mb-4">Recent Transactions</h2>
    <Table.Root>
        <Table.Caption>A list of your recent transactions.</Table.Caption>
        <Table.Header>
            <Table.Row>
                <Table.Head class="w-[100px]">Description</Table.Head>
                <Table.Head>Counterparty</Table.Head>
                <Table.Head>Amount</Table.Head>
                <Table.Head class="text-right">Date</Table.Head>
            </Table.Row>
        </Table.Header>
        <Table.Body>
            {#each data.transactions as transaction (transaction.transaction_id)}
                <Table.Row>
                    <Table.Cell class="font-medium">{transaction.description}</Table.Cell>
                    <Table.Cell>{transaction.counterparty}</Table.Cell>
                    <Table.Cell>{transaction.amount}</Table.Cell>
                    <Table.Cell class="text-right">{transaction.date}</Table.Cell>
                </Table.Row>
            {/each}
        </Table.Body>
    </Table.Root>
</div>

<button
    class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600"
    onclick={openAddBankModal}
>
    Add Bank
</button>

{#if addBankModalVisible}
    <div class="modal fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
        <div class="modal-content bg-white p-6 rounded-lg shadow-lg w-1/3">
            <h3 class="text-lg font-bold mb-4">Add a New Bank</h3>
            <form onsubmit={preventDefault(addBank)}>
                <label class="block mb-2">
                    Bank Name:
                    <input type="text" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required />
                </label>
                <label class="block mb-2">
                    Initial Balance:
                    <input type="number" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required />
                </label>
                <div class="mt-4 flex justify-end gap-2">
                    <button type="button" class="px-4 py-2 bg-gray-400 text-white rounded-lg shadow-md hover:bg-gray-500" onclick={closeAddBankModal}>
                        Cancel
                    </button>
                    <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600">
                        Add Bank
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}
