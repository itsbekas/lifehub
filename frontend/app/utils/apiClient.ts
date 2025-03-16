import { getSession } from "~/utils/session";

const BASE_URL = process.env.BACKEND_URL;

export async function fetchWithAuth(
  endpoint: string,
  init: RequestInit = {},
  request?: Request
) {
  const session = await getSession(request?.headers.get("Cookie"));
  const token = session.get("access_token");

  if (!token) {
    throw new Error("Authentication token not found");
  }

  // Ensure headers exist and include the Authorization token
  const headers = {
    ...init.headers,
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };

  // Construct the full URL
  const url = `${BASE_URL}/api/v0${endpoint}`;

  // Perform the fetch
  return fetch(url, {
    ...init,
    method: init.method || "GET", // Default to GET if no method is provided
    headers,
  });
}
