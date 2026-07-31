/**
 * Layout principal da aplicação.
 *
 * Responsabilidades:
 * - Exibir a barra lateral de navegação.
 * - Exibir o cabeçalho.
 * - Renderizar o conteúdo das páginas protegidas.
 */

import { Outlet } from "react-router-dom";

import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";

import "./MainLayout.css";

/**
 * Layout utilizado por todas as páginas autenticadas.
 */
function MainLayout() {
    return (
        <div className="layout">
            <Sidebar />

            <div className="layout-content">
                <Header />

                <main
                    className="page-content"
                    role="main"
                >
                    <Outlet />
                </main>
            </div>
        </div>
    );
}

export default MainLayout;