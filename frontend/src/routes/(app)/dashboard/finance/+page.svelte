<script lang="ts">
    import type { BankBalance, BankInstitution, BankTransaction, BudgetCategory } from "@/lib/types/finance";
    import * as Table from "@/components/ui/table";
    import * as Card from "@/components/ui/card";
    import { Button } from "@/components/ui/button";

    // Define the Props interface as requested
    interface Props {
        data: { balances: BankBalance[], transactions: BankTransaction[], banks: BankInstitution[], budgetCategories: BudgetCategory[] };
    }

    // Use the $props rune to destructure the props based on the defined interface
    let { data }: Props = $props();

    // Sort transactions by date
    data.transactions = data.transactions.sort((a, b) => Date.parse(b.date) - Date.parse(a.date));

    // Reactive state for managing modal visibility using $state
    let addBankModalVisible = $state(false);
    let addCategoryModalVisible = $state(false);
    let activeTab = $state("budget");

    function openAddBankModal() {
        addBankModalVisible = true;
    }

    function closeAddBankModal() {
        addBankModalVisible = false;
    }

    function openAddCategoryModal() {
        addCategoryModalVisible = true;
    }

    function closeAddCategoryModal() {
        addCategoryModalVisible = false;
    }

    function addBank() {
        // Logic to add bank goes here
        closeAddBankModal();
    }

    function addCategory() {
        // Logic to add category goes here
        closeAddCategoryModal();
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
    <button class="tab px-4 py-2 text-lg font-medium text-gray-700 border-b-2 border-transparent hover:text-gray-900 focus:outline-none" class:active={activeTab === 'budget'} onclick={() => activeTab = 'budget'}>Budget</button>
    <button class="tab px-4 py-2 text-lg font-medium text-gray-700 border-b-2 border-transparent hover:text-gray-900 focus:outline-none" class:active={activeTab === 'transactions'} onclick={() => activeTab = 'transactions'}>Transactions</button>
</div>

{#if activeTab === 'budget'}
    <div class="budget-section mb-6">
        <h2 class="text-xl font-bold mb-4">Budget Overview</h2>
        <Button class="mb-4" onclick={openAddCategoryModal}>Add Category</Button>
        <div class="budget-categories grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each data.budgetCategories as category (category.id)}
                <Card.Root class="w-full">
                    <Card.Header>
                        <Card.Title>{category.name}</Card.Title>
                    </Card.Header>
                    <Card.Content>
                        <ul class="space-y-2">
                            {#each category.subcategories as subcategory (subcategory.id)}
                                <li class="border-b border-gray-200 pb-2">
                                    <div class="flex justify-between">
                                        <span class="font-medium text-gray-800">{subcategory.name}</span>
                                        <span class="text-gray-600">Budgeted: {subcategory.budgeted}</span>
                                    </div>
                                    <div class="flex justify-between text-sm text-gray-600">
                                        <span>Spent: {subcategory.spent}</span>
                                        <span>Available: {subcategory.available}</span>
                                    </div>
                                </li>
                            {/each}
                        </ul>
                    </Card.Content>
                </Card.Root>
            {/each}
        </div>
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
                    <button class="border border-gray-200 rounded-lg p-4 bg-gray-50 flex items-center justify-center cursor-pointer hover:bg-gray-100 focus:outline-none" onclick={openAddBankModal}>
                        <h3 class="text-md font-medium text-gray-800">Add a Bank</h3>
                    </button>
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
                            <Table.Head>Sub-category</Table.Head>
                            <Table.Head>Amount</Table.Head>
                            <Table.Head class="text-right">Date</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each data.transactions as transaction (transaction.transaction_id)}
                            <Table.Row>
                                <Table.Cell class="font-medium">{transaction.user_description ? transaction.user_description : `${transaction.description} (${transaction.counterparty})`}</Table.Cell>
                                <Table.Cell>{#each data.budgetCategories as category}{#each category.subcategories as subcategory}{#if subcategory.id === transaction.subcategory_id}{subcategory.name}{/if}{/each}{/each}</Table.Cell>
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
        <div class="modal-content bg-white p-6 rounded-lg shadow-lg w-1/4">
            <h3 class="text-lg font-bold mb-4">Add a New Bank</h3>
            <form method="POST" action="?/add-bank" onsubmit={preventDefault(addBank)}>
                <label class="block mb-2">
                    Bank Name:
                    <select name="bankId" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required>
                        <option value="" disabled selected>Select a bank</option>
                        {#each data.banks as bank}
                            <option value="{bank}">{bank.name}</option>
                        {/each}
                    </select>
                </label>
                
                <div class="mt-4 flex justify-end gap-2">
                    <Button variant="secondary" onclick={closeAddBankModal}>Cancel</Button>
                    <Button type="submit">Add Bank</Button>
                </div>
            </form>
        </div>
    </div>
{/if}

{#if addCategoryModalVisible}
    <div class="modal fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
        <div class="modal-content bg-white p-6 rounded-lg shadow-lg w-1/3">
            <h3 class="text-lg font-bold mb-4">Add a New Category</h3>
            <form onsubmit={preventDefault(addCategory)}>
                <label class="block mb-2">
                    Category Name:
                    <input type="text" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required />
                </label>
                <div class="mt-4 flex justify-end gap-2">
                    <Button variant="secondary" onclick={closeAddCategoryModal}>Cancel</Button>
                    <Button type="submit">Add Category</Button>
                </div>
            </form>
        </div>
    </div>
{/if}
