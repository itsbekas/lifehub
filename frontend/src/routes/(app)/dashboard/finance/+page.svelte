<script lang="ts">
    import type { BankBalance, BankInstitution, BankTransaction, BankTransactionFilter, BudgetCategory } from "@/lib/types/finance";
    import * as Table from "@/components/ui/table";
    import * as Card from "@/components/ui/card";
    import { Button } from "@/components/ui/button";

    // Define the Props interface as requested
    interface Props {
        data: {
            balances: BankBalance[],
            transactions: BankTransaction[],
            banks: BankInstitution[],
            budgetCategories: BudgetCategory[],
            filters: BankTransactionFilter[],
        };
    }

    // Use the $props rune to destructure the props based on the defined interface
    let { data }: Props = $props();

    // Sort transactions by date
    data.transactions = data.transactions.sort((a, b) => Date.parse(b.date) - Date.parse(a.date));

    // Reactive state for managing modal visibility using $state
    let addBankModalVisible = $state(false);
    let addCategoryModalVisible = $state(false);
    let addSubCategoryModalVisible = $state(false);
    let activeTab = $state("budget");
    let selectedCategoryId = $state<string | null>(null);

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

    function openAddSubCategoryModal(categoryId: string) {
        selectedCategoryId = categoryId;
        addSubCategoryModalVisible = true;
    }

    function closeAddSubCategoryModal() {
        addSubCategoryModalVisible = false;
        selectedCategoryId = null;
    }

    function getSubcategoryById(subcategoryId: string) {
        for (const category of data.budgetCategories) {
            for (const subcategory of category.subcategories) {
                if (subcategory.id === subcategoryId) {
                    return subcategory;
                }
            }
        }
    }

    function getTransactionById(transactionId: string) {
        return data.transactions.find(transaction => transaction.id === transactionId);
    }

let editTransactionModalVisible = $state(false);
let selectedTransaction = $state<BankTransaction | null>(null);

function openEditTransactionModal(transaction: BankTransaction) {
    selectedTransaction = transaction;
    editTransactionModalVisible = true;
}

function closeEditTransactionModal() {
    editTransactionModalVisible = false;
    selectedTransaction = null;
}
let addFilterModalVisible = $state(false);
let editFilterModalVisible = $state(false);
let selectedFilterId = $state<string | null>(null);

function openAddFilterModal() {
    addFilterModalVisible = true;
}

function closeAddFilterModal() {
    addFilterModalVisible = false;
}

function openEditFilterModal(filterId: string) {
    selectedFilterId = filterId;
    editFilterModalVisible = true;
}

function closeEditFilterModal() {
    editFilterModalVisible = false;
    selectedFilterId = null;
}
</script>

<div class="tabs mb-6">
    <button class="tab px-4 py-2 text-lg font-medium text-gray-700 border-b-2 border-transparent hover:text-gray-900 focus:outline-none" class:active={activeTab === 'budget'} onclick={() => activeTab = 'budget'}>Budget</button>
    <button class="tab px-4 py-2 text-lg font-medium text-gray-700 border-b-2 border-transparent hover:text-gray-900 focus:outline-none" class:active={activeTab === 'transactions'} onclick={() => activeTab = 'transactions'}>Transactions</button>
    <button class="tab ml-auto px-4 py-2 text-lg font-medium text-gray-700 border-b-2 border-transparent hover:text-gray-900 focus:outline-none" class:active={activeTab === 'settings'} onclick={() => activeTab = 'settings'}>Settings</button>
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
                                        <span class="text-gray-600">Budgeted: {subcategory.budgeted.toFixed(2)}€</span>
                                    </div>
                                    <div class="flex justify-between text-sm text-gray-600">
                                        <span>Spent: {subcategory.spent.toFixed(2)}€</span>
                                        <span>Available: {subcategory.available.toFixed(2)}€</span>
                                    </div>
                                </li>
                            {/each}
                        </ul>
                        <Button class="mt-2" onclick={openAddSubCategoryModal.bind(null, category.id)}>Add Sub-category</Button>
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
                    {#each data.balances as balance (balance.account_id)}
                        <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
                            <h3 class="text-md font-medium mb-1 truncate text-gray-800">{balance.bank}</h3>
                            <p class="text-gray-600 text-sm">Balance: {balance.balance.toFixed(2)}€</p>
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
                            <Table.Head class="w-auto">Description</Table.Head>
                            <Table.Head>Sub-category</Table.Head>
                            <Table.Head>Amount</Table.Head>
                            <Table.Head class="text-right">Date</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each data.transactions as transaction (transaction.id)}
                            <Table.Row>
                                <Table.Cell class="font-medium whitespace-normal break-words">{transaction.user_description ? transaction.user_description : `${transaction.description} (${transaction.counterparty})`}</Table.Cell>
                                <Table.Cell>{getSubcategoryById(transaction.subcategory_id!)?.name}</Table.Cell>
                                <Table.Cell>{transaction.amount.toFixed(2)}€</Table.Cell>
                                <Table.Cell class="text-right">{new Date(transaction.date).toLocaleDateString()}</Table.Cell>
                            <Table.Cell>
                                <Button variant="outline" onclick={() => openEditTransactionModal(transaction)}>Edit</Button>
                            </Table.Cell>
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
            <form method="POST" action="?/addBank">
                <label class="block mb-2">
                    Bank Name:
                    <select name="bankId" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required>
                        <option value="" disabled selected>Select a bank</option>
                        {#each data.banks as bank}
                            <option value="{bank.id}">{bank.name}</option>
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
            <form method="POST" action="?/addCategory">
                <label class="block mb-2">
                    Category Name:
                    <input name="name" type="text" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required />
                </label>
                <div class="mt-4 flex justify-end gap-2">
                    <Button variant="secondary" onclick={closeAddCategoryModal}>Cancel</Button>
                    <Button type="submit">Add Category</Button>
                </div>
            </form>
        </div>
    </div>
{/if}

{#if editTransactionModalVisible}
    <div class="modal fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
        <div class="modal-content bg-white p-6 rounded-lg shadow-lg w-1/3">
            <h3 class="text-lg font-bold mb-4">Edit Transaction</h3>
            <form method="POST" action="?/editTransaction">
                <input type="hidden" name="transactionId" value={selectedTransaction?.id} />
                <input type="hidden" name="accountId" value={selectedTransaction?.account_id} />
                <label class="block mb-2">
                    Description:
                    <input name="description" type="text" class="border border-gray-300 rounded-lg w-full p-2 mt-1" value={getTransactionById(selectedTransaction!.id)?.user_description || ''} />
                </label>
                <label class="block mb-2">
                    Sub-category:
                    <select name="subcategoryId" class="border border-gray-300 rounded-lg w-full p-2 mt-1">
                        <option value="" disabled selected>Select a sub-category</option>
                        {#each data.budgetCategories as category}
                            {#each category.subcategories as subcategory}
                                <option value={subcategory.id} selected={subcategory.id === getTransactionById(selectedTransaction!.id)?.subcategory_id}>{subcategory.name}</option>
                            {/each}
                        {/each}
                    </select>
                </label>
                <label class="block mb-2">
                    Amount:
                    <input name="amount" type="number" step="0.01" class="border border-gray-300 rounded-lg w-full p-2 mt-1" value={getTransactionById(selectedTransaction!.id)?.amount || 0} />
                </label>
                <div class="mt-4 flex justify-end gap-2">
                    <Button variant="secondary" onclick={closeEditTransactionModal}>Cancel</Button>
                    <Button type="submit">Save Changes</Button>
                </div>
            </form>
        </div>
    </div>
{/if}

{#if activeTab === 'settings'}
    <div class="settings-section mb-6">
        <h2 class="text-xl font-bold mb-4">Settings</h2>
        <div class="filters-section mb-6">
            <h3 class="text-lg font-semibold mb-2">Manage Filters</h3>
            <p class="text-gray-700 mb-4">Create filters to help auto-categorize and auto-rename transactions based on their descriptions.</p>
            <Button onclick={() => openAddFilterModal()}>Add Filter</Button>
            <div class="filters-list mt-4">
                {#each data.filters as filter (filter.id)}
                    <div class="filter-item border border-gray-300 rounded-lg p-4 mb-4">
                        <div class="flex justify-between items-center">
                            <div>
                                <p class="font-medium">{filter.description}</p>
                                {#if filter.subcategory_id}
                                    <p class="text-sm text-gray-600">Sub-category ID: {getSubcategoryById(filter.subcategory_id)?.name}</p>
                                {/if}
                                {#if filter.description}
                                    <p class="text-sm text-gray-600">Filter: {filter.filter}</p>
                                {/if}
                            </div>
                            <Button variant="outline" onclick={() => openEditFilterModal(filter.id)}>Edit</Button>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
{/if}

{#if addFilterModalVisible}
    <div class="modal fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
        <div class="modal-content bg-white p-6 rounded-lg shadow-lg w-1/3">
            <h3 class="text-lg font-bold mb-4">Add a New Filter</h3>
            <form method="POST" action="?/addFilter">
                <label class="block mb-2">
                    Filter:
                    <input type="text" name="filter" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required />
                </label>
                <label class="block mb-2">
                    Sub-category:
                    <select name="subcategoryId" class="border border-gray-300 rounded-lg w-full p-2 mt-1">
                        <option value="" disabled selected>Select a sub-category</option>
                        {#each data.budgetCategories as category}
                            {#each category.subcategories as subcategory}
                                <option value={subcategory.id}>{subcategory.name}</option>
                            {/each}
                        {/each}
                    </select>
                </label>
                <label class="block mb-2">
                    Rename to (optional):
                    <input type="text" name="description" class="border border-gray-300 rounded-lg w-full p-2 mt-1" />
                </label>
                <div class="mt-4 flex justify-end gap-2">
                    <Button variant="secondary" onclick={closeAddFilterModal}>Cancel</Button>
                    <Button type="submit">Add Filter</Button>
                </div>
            </form>
        </div>
    </div>
{/if}

{#if editFilterModalVisible}
    <div class="modal fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
        <div class="modal-content bg-white p-6 rounded-lg shadow-lg w-1/3">
            <h3 class="text-lg font-bold mb-4">Edit Filter</h3>
            <form method="POST" action="?/editFilter">
                <input type="hidden" name="filterId" value={selectedFilterId} />
                <label class="block mb-2">
                    Filter:
                    <input type="text" name="filter" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required value={data.filters.find(filter => filter.id === selectedFilterId)?.filter || ''} />
                </label>
                <label class="block mb-2">
                    Sub-category:
                    <select name="subcategoryId" class="border border-gray-300 rounded-lg w-full p-2 mt-1">
                        <option value="" disabled selected>Select a sub-category</option>
                        {#each data.budgetCategories as category}
                            {#each category.subcategories as subcategory}
                                <option value={subcategory.id}>{subcategory.name}</option>
                            {/each}
                        {/each}
                    </select>
                </label>
                <label class="block mb-2">
                    Rename to (optional):
                    <input type="text" name="description" class="border border-gray-300 rounded-lg w-full p-2 mt-1" value={data.filters.find(filter => filter.id === selectedFilterId)?.description || ''} />
                </label>
                <div class="mt-4 flex justify-end gap-2">
                    <Button variant="secondary" onclick={closeEditFilterModal}>Cancel</Button>
                    <Button type="submit">Save Changes</Button>
                </div>
            </form>
        </div>
    </div>
{/if}

{#if addSubCategoryModalVisible}
    <div class="modal fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
        <div class="modal-content bg-white p-6 rounded-lg shadow-lg w-1/3">
            <h3 class="text-lg font-bold mb-4">Add a New Sub-category</h3>
            <form method="POST" action="?/addSubCategory">
                <input type="hidden" name="categoryId" value={selectedCategoryId} />
                <label class="block mb-2">
                    Sub-category Name:
                    <input name="name" type="text" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required />
                </label>
                <label class="block mb-2">
                    Budgeted Amount:
                    <input name="amount" type="number" step="0.01" class="border border-gray-300 rounded-lg w-full p-2 mt-1" required />
                </label>
                <div class="mt-4 flex justify-end gap-2">
                    <Button variant="secondary" onclick={closeAddSubCategoryModal}>Cancel</Button>
                    <Button type="submit">Add Sub-category</Button>
                </div>
            </form>
        </div>
    </div>
{/if}
