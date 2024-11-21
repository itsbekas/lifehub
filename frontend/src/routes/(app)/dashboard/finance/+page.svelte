<script lang="ts">
    import type { BankBalance, BankTransaction } from "@/lib/types/finance";
    import * as Table from "@/components/ui/table";
    import * as Card from "@/components/ui/card";

    // Define the Props interface as requested
    interface Props {
        data: { balances: BankBalance[], transactions: BankTransaction[], banks: string[] };
    }

    // Use the $props rune to destructure the props based on the defined interface
    let { data }: Props = $props();

    // Sort transactions by date
    data.transactions = data.transactions.sort((a, b) => Date.parse(b.date) - Date.parse(a.date));

    // Reactive state for managing modal visibility using $state
    let addBankModalVisible = $state(false);
    let activeTab = $state("budget");

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

<div class="tabs mb-6">
    <button class="tab px-4 py-2 text-lg font-semibold" class:active={activeTab === 'budget'} onclick={() => activeTab = 'budget'}>Budget</button>
    <button class="tab px-4 py-2 text-lg font-semibold" class:active={activeTab === 'transactions'} onclick={() => activeTab = 'transactions'}>Transactions</button>
</div>

{#if activeTab === 'budget'}
    <div class="budget-section mb-6">
        <h2 class="text-xl font-bold mb-4">Budget Overview</h2>
        <p class="text-gray-700">This is where the budget information will be displayed.</p>
    </div>
{/if}

{#if activeTab === 'transactions'}
    <div class="balances-section mb-6">
        <Card.Root class="w-full">
            <Card.Header>
                <Card.Title>Bank Balances</Card.Title>
                <Card.Description>An overview of your bank balances.</Card.Description>
            </Card.Header>
            <Card.Content class="p-4">
                <div class="balances grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {#each data.balances as balance (balance.bank)}
                        <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
                            <h3 class="text-md font-medium mb-1 truncate text-gray-800">{balance.bank}</h3>
                            <p class="text-gray-600 text-sm">Balance: {balance.balance}</p>
                        </div>
                    {/each}
                    <div class="border border-gray-200 rounded-lg p-4 bg-gray-50 flex items-center justify-center cursor-pointer hover:bg-gray-100" onclick={openAddBankModal}>
                        <h3 class="text-md font-medium text-gray-800">Add a Bank</h3>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>
    </div>

    <div class="transactions-section">
        <Card.Root class="w-full">
            <Card.Header>
                <Card.Title>Recent Transactions</Card.Title>
                <Card.Description>A list of your recent transactions.</Card.Description>
            </Card.Header>
            <Card.Content>
                <Table.Root>
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
                                <Table.Cell class="text-right">{new Date(transaction.date).toLocaleDateString()}</Table.Cell>
                            </Table.Row>
                        {/each}
                    </Table.Body>
                </Table.Root>
            </Card.Content>
        </Card.Root>
    </div>
{/if}

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
