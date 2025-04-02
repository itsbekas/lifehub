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
  console.log(token);
  console.log(!!token);
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
    httpOnly: true, // Ensures the cookie is only accessible via HTTP(S) and not JavaScript, enhancing security.
    secure: process.env.NODE_ENV === "production", // Ensures the cookie is only sent over HTTPS, preventing it from being transmitted over insecure connections.
    sameSite: "Strict", // Prevents the cookie from being sent with cross-site requests, mitigating CSRF attacks.
  });
};
