import { fetchWithAuth } from "~/utils/apiClient";
import { TransactionsTable } from "~/components/TransactionsTable";
import type { Route } from "./+types/dashboard.finance";

export type Transaction = {
  id: string;
  account_id: string;
  amount: number;
  date: string;
  description: string;
  counterparty: string;
  subcategory_id: string;
  user_description: string;
};

export async function loader({ request }: Route.LoaderArgs) {
  const res = await fetchWithAuth(
    "/finance/bank/transactions",
    undefined,
    request
  );
  if (!res.ok) {
    throw new Error(`Failed to fetch transactions: ${res.statusText}`);
  }

  const transactions: Transaction[] = await res.json();

  return transactions;
}

export default function FinancePage({ loaderData }: Route.ComponentProps) {
  const transactions = loaderData;

  return (
    <div>
      <h1>Finance Dashboard</h1>
      <TransactionsTable transactions={transactions} />
    </div>
  );
}
