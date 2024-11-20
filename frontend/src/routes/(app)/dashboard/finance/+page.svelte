<script lang="ts">
    import type { BankBalance, BankTransaction } from "@/lib/types/finance";

interface Props {
    data: { balances: BankBalance[], transactions: BankTransaction[] };
}

let { data }: Props = $props();

</script>

<div class="balances flex flex-wrap gap-4">
    {#each data.balances as balance}
        <div class="card border border-gray-300 rounded-lg p-4 w-48 shadow-md">
            <h3 class="text-lg font-semibold mb-2">{balance.bank}</h3>
            <p class="text-gray-700">Balance: {balance.balance}</p>
        </div>
    {/each}
</div>
