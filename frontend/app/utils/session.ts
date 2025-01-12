import { createCookieSessionStorage } from "react-router";

type SessionData = {
  access_token: string;
};

type SessionFlashData = {
  error: string;
};

// Configure session storage
export const { getSession, commitSession, destroySession } =
  createCookieSessionStorage<SessionData, SessionFlashData>({
    cookie: {
      name: "access_token",
      secure: process.env.NODE_ENV === "production",
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60 * 24 * 7, // 7 days
      secrets: [import.meta.env.VITE_SESSION_SECRET as string],
    },
  });
