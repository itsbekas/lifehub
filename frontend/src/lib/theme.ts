import { createTheme, type MantineColorsTuple } from "@mantine/core";

// Define custom colors
const primary: MantineColorsTuple = [
  "#f0f9ff",
  "#e0f2fe",
  "#bae6fd",
  "#7dd3fc",
  "#38bdf8",
  "#0ea5e9",
  "#0284c7",
  "#0369a1",
  "#075985",
  "#0c4a6e",
];

const success: MantineColorsTuple = [
  "#f0fdf4",
  "#dcfce7",
  "#bbf7d0",
  "#86efac",
  "#4ade80",
  "#22c55e",
  "#16a34a",
  "#15803d",
  "#166534",
  "#14532d",
];

const warning: MantineColorsTuple = [
  "#fffbeb",
  "#fef3c7",
  "#fde68a",
  "#fcd34d",
  "#fbbf24",
  "#f59e0b",
  "#d97706",
  "#b45309",
  "#92400e",
  "#78350f",
];

const error: MantineColorsTuple = [
  "#fef2f2",
  "#fee2e2",
  "#fecaca",
  "#fca5a5",
  "#f87171",
  "#ef4444",
  "#dc2626",
  "#b91c1c",
  "#991b1b",
  "#7f1d1d",
];

// Create the theme
export const theme = createTheme({
  primaryColor: "primary",
  colors: {
    primary,
    success,
    warning,
    error,
  },
  fontFamily: "Inter, sans-serif",
  fontFamilyMonospace: "Monaco, Courier, monospace",
  headings: {
    fontFamily: "Inter, sans-serif",
    fontWeight: "600",
  },
  defaultRadius: "md",
  components: {
    Card: {
      defaultProps: {
        withBorder: true,
        radius: "md",
        padding: "lg",
      },
    },
    Button: {
      defaultProps: {
        radius: "md",
      },
    },
    Table: {
      styles: {
        root: {
          borderCollapse: "separate",
          borderSpacing: "0",
        },
      },
    },
  },
});
