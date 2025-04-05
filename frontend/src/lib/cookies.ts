import Cookie from "js-cookie";

export const getCookie = (key: string): string | undefined => {
  return Cookie.get(key);
};

export const setCookie = (
  key: string,
  value: string,
  options?: Cookies.CookieAttributes,
): void => {
  Cookie.set(key, value, options);
};

export const removeCookie = (key: string): void => {
  Cookie.remove(key);
};

export const isAuthenticated = (): boolean => {
  const token = getCookie("authToken");
  return !!token; // Returns true if the token exists, indicating the user is authenticated.
};

export const logoutUser = (): void => {
  // Remove the auth token from cookies
  removeCookie("authToken");
};

/**
 * Logs in a user by setting an authentication token in cookies.
 *
 * @param token - The authentication token to be stored in the cookies.
 *                This token is used to identify and authenticate the user.
 * @param expiresAt - The expiration date and time for the cookie.
 *                    This determines how long the authentication token will remain valid.
 */
export const loginUser = (token: string, expiresAt: Date): void => {
  // Set the auth token in cookies
  setCookie("authToken", token, {
    expires: expiresAt,
    // In development, we need to allow JavaScript access to cookies for cross-origin requests
    httpOnly: process.env.NODE_ENV === "production",
    // Only use secure in production (HTTPS)
    secure: process.env.NODE_ENV === "production",
    // Use Lax in development for cross-origin requests, Strict in production
    sameSite: process.env.NODE_ENV !== "production" ? "Lax" : "Strict",
  });
};
