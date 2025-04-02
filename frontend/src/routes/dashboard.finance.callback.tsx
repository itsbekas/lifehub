import type { Route } from "./+types/dashboard.finance.callback";
import { redirect } from "react-router";
import { fetchWithAuth } from "~/utils/apiClient";

export async function loader({ request }: Route.LoaderArgs) {
  const url = new URL(request.url);
  const ref = url.searchParams.get("ref");

  if (!ref) {
    return redirect("/error?message=Missing+ref");
  }

  const response = await fetchWithAuth(
    `/finance/bank/callback?ref=${ref}`,
    {
      method: "POST",
    },
    request
  );

  if (!response.ok) {
    const errorData = await response.json();
    return redirect(
      `/error?message=${errorData.message || "Failed to add bank account."}`
    );
  }

  return redirect("/dashboard/finance");
}
