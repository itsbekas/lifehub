import axios from "axios";
import { QueryClient } from "@tanstack/react-query";
import { getCookie } from "./cookies";

// Determine the base URL based on the environment
const getBaseUrl = () => {
  // In development, use the backend server URL
  if (process.env.NODE_ENV !== "production") {
    return "http://localhost:8000/api/v0";
  }
  // In production, use relative URL (same host)
  return "/api/v0";
};

// Create an axios instance that automatically prefixes /api/v0/ to requests
const axiosInstance = axios.create({
  baseURL: getBaseUrl(),
  headers: {
    "Content-Type": "application/json",
  },
  // Enable credentials (cookies) for cross-origin requests
  withCredentials: process.env.NODE_ENV !== "production",
});

// Add an interceptor to automatically add the auth token when available
axiosInstance.interceptors.request.use((config) => {
  const token = getCookie("authToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor to handle 401 Unauthorized responses
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    // If we get a 401 Unauthorized response, redirect to login
    if (error.response && error.response.status === 401) {
      // Remove the auth token as it's likely invalid
      removeCookie("authToken");

      // Redirect to login page
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

// Create a function to make requests without authentication
export const createUnauthenticatedRequest = () => {
  // Create a new instance without the auth interceptor
  return axios.create({
    baseURL: getBaseUrl(),
    headers: {
      "Content-Type": "application/json",
    },
    // Enable credentials (cookies) for cross-origin requests
    withCredentials: process.env.NODE_ENV !== "production",
  });
};

// Export the axios instance for direct use
export const api = axiosInstance;

// Create a queryClient instance
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
    mutations: {
      retry: 0,
    },
  },
});

export default queryClient;
