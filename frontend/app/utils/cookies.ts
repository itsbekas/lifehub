import { createCookie } from "react-router";

export const accessTokenCookie = createCookie("access_token", {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "lax",
  path: "/",
  maxAge: 3600, // 1 hour
});
