/**
 * Configuração do Vite para o frontend do GymFlow.
 *
 * Responsabilidades:
 * - Configurar o React.
 * - Definir alias para facilitar os imports.
 * - Configurar o servidor de desenvolvimento.
 * - Preparar a aplicação para build de produção.
 */

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

export default defineConfig({
    plugins: [
        react(),
    ],

    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },

    server: {
        host: "0.0.0.0",
        port: 5173,
        open: true,
    },

    preview: {
        port: 4173,
    },

    build: {
        sourcemap: false,
        outDir: "dist",
        emptyOutDir: true,
    },
});