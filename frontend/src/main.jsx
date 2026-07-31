/**
 * Ponto de entrada da aplicação GymFlow.
 *
 * Responsabilidades:
 * - Inicializar a aplicação React.
 * - Carregar os estilos globais.
 * - Registrar os Providers.
 * - Renderizar a aplicação.
 */

import React from "react";
import ReactDOM from "react-dom/client";
import { Toaster } from "react-hot-toast";

import { AuthProvider } from "@/contexts/AuthContext";
import AppRoutes from "@/routes/AppRoutes";

import "./index.css";

/**
 * Elemento raiz da aplicação.
 */
const rootElement = document.getElementById("root");

if (!rootElement) {
    throw new Error("Elemento '#root' não encontrado.");
}

ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
        <AuthProvider>
            <AppRoutes />

            <Toaster
                position="top-right"
                reverseOrder={false}
                gutter={12}
                toastOptions={{
                    duration: 4000,
                    style: {
                        background: "#ffffff",
                        color: "#1f2937",
                        border: "1px solid #e5e7eb",
                        borderRadius: "10px",
                        fontSize: "14px",
                    },
                    success: {
                        iconTheme: {
                            primary: "#16a34a",
                            secondary: "#ffffff",
                        },
                    },
                    error: {
                        iconTheme: {
                            primary: "#dc2626",
                            secondary: "#ffffff",
                        },
                    },
                }}
            />
        </AuthProvider>
    </React.StrictMode>,
);