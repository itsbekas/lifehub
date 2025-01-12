import { getSession } from "~/utils/session";

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

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

  // Add the Authorization header
  const headers = {
    ...init.headers,
    Authorization: `Bearer ${token}`,
  };

  // Construct the full URL
  const url = `${BASE_URL}/api/v0${endpoint}`;

  // Perform the fetch
  return fetch(url, {
    ...init,
    headers,
  });
}
