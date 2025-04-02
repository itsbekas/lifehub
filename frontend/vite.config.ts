// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { TanStackRouterVite } from "@tanstack/router-plugin/vite";
import autoprefixer from "autoprefixer";
import tailwindcss from "tailwindcss";
import { resolve } from "node:path";

// https://vitejs.dev/config/
export default defineConfig({
  css: {
    postcss: {
      plugins: [tailwindcss, autoprefixer],
    },
  },
  plugins: [
    TanStackRouterVite({ target: "react", autoCodeSplitting: true }),
    react(),
  ],
  resolve: {
    alias: {
      // /esm/icons/index.mjs only exports the icons statically, so no separate chunks are created
      "@tabler/icons-react": "@tabler/icons-react/dist/esm/icons/index.mjs",
      "~": resolve(__dirname, "./src"),
    },
  },
});
