/**
 * Cabeçalho principal da aplicação.
 *
 * Responsabilidades:
 * - Exibir o título da aplicação.
 * - Exibir informações do usuário autenticado.
 * - Disponibilizar ações globais.
 */

import { useLocation } from "react-router-dom";

import { useAuthContext } from "@/contexts/AuthContext";
import { ROUTES } from "@/constants/routes";

import "./Header.css";

/**
 * Títulos das páginas.
 */
const PAGE_TITLES = Object.freeze({
    [ROUTES.DASHBOARD]: "Dashboard",
    [ROUTES.CHECKINS]: "Check-ins",
    [ROUTES.USERS]: "Usuários",
});

/**
 * Cabeçalho das páginas autenticadas.
 */
function Header() {
    const location = useLocation();

    const {
        user,
        logout,
    } = useAuthContext();

    const pageTitle =
        PAGE_TITLES[location.pathname] ?? "GymFlow";

    return (
        <header className="header">
            <div className="header-left">
                <h1 className="header-title">
                    {pageTitle}
                </h1>

                <span className="header-subtitle">
                    Sistema de gerenciamento de academia
                </span>
            </div>

            <div className="header-right">
                <div className="header-user">
                    <span className="header-user-name">
                        {user?.name ?? "Usuário"}
                    </span>

                    <span className="header-user-role">
                        {user?.role ?? ""}
                    </span>
                </div>

                <button
                    type="button"
                    className="logout-button"
                    aria-label="Sair da aplicação"
                    onClick={logout}
                >
                    Sair
                </button>
            </div>
        </header>
    );
}

export default Header;