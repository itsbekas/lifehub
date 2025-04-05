# Lifehub Frontend

A modern frontend for the Lifehub application, built with React and TanStack Router.

## Tech Stack

- **React 19** - Modern UI library
- **TanStack Router** - Type-safe routing for React applications
- **TanStack Query** - Data fetching and state management
- **Mantine UI** - Component library for building the user interface
- **Axios** - HTTP client for API requests
- **Vite** - Fast build tool and development server

## Project Structure

- `src/routes` - Route components following the TanStack Router file-based routing convention
- `src/components` - Reusable UI components
- `src/hooks` - Custom React hooks for data fetching and business logic
- `src/lib` - Utility functions and configuration
- `src/styles` - CSS modules and global styles

## Features Implemented

- **Authentication** - Login, signup, and token-based authentication
- **Dashboard Layout** - Common layout for all dashboard pages with authentication protection
- **Finance Dashboard** - View and manage financial data:
  - Transaction listing and categorization
  - Budget categories and subcategories
  - Bank account balances
  - Bank account integration

## Development Approach

The application uses a client-side rendering approach with TanStack Router and TanStack Query:

- **Routing** - File-based routing with TanStack Router
- **Data Fetching** - Client-side data fetching with TanStack Query
- **Authentication** - Token-based authentication with cookie storage
- **API Communication** - Axios for API requests with interceptors for authentication

## Getting Started

1. Install dependencies:

   ```
   npm install
   ```

2. Start the development server:

   ```
   npm run dev
   ```

3. Build for production:
   ```
   npm run build
   ```

## Authentication Flow

Authentication is handled at multiple levels:

1. **Route Protection** - Dashboard routes check for authentication before rendering
2. **API Requests** - Axios interceptors add authentication tokens to requests
3. **Error Handling** - 401 responses automatically redirect to the login page

## Future Improvements

- Complete implementation of remaining dashboard modules
- Add more comprehensive error handling
- Implement offline support
- Add comprehensive test coverage
