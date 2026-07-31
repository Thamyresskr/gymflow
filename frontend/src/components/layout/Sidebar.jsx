/**
 * Barra lateral de navegação da aplicação.
 *
 * Responsabilidades:
 * - Exibir a identidade da aplicação.
 * - Exibir o usuário autenticado.
 * - Disponibilizar a navegação principal.
 * - Destacar automaticamente a rota ativa.
 * - Encerrar a sessão.
 */

import { NavLink } from "react-router-dom";

import { useAuthContext } from "@/contexts/AuthContext";
import { ROUTES } from "@/routes/AppRoutes";

import "./Sidebar.css";

/**
 * Itens do menu principal.
 */
const MENU_ITEMS = [
    {
        label: "Dashboard",
        path: ROUTES.DASHBOARD,
    },
    {
        label: "Check-ins",
        path: ROUTES.CHECKINS,
    },
    {
        label: "Usuários",
        path: ROUTES.USERS,
        roles: ["ADMIN"],
    },
];

/**
 * Barra lateral da aplicação.
 */
function Sidebar() {
    const {
        user,
        logout,
    } = useAuthContext();

    const menu = MENU_ITEMS.filter((item) => {
        if (!item.roles) {
            return true;
        }

        return item.roles.includes(user?.role);
    });

    return (
        <aside
            className="sidebar"
            aria-label="Barra lateral"
        >
            <div className="sidebar-logo">
                <h2>GymFlow</h2>
            </div>

            <div className="sidebar-user">
                <strong>{user?.name ?? "Usuário"}</strong>

                <span>{user?.role ?? ""}</span>
            </div>

            <nav
                className="sidebar-nav"
                aria-label="Menu principal"
            >
                {menu.map(({ label, path }) => (
                    <NavLink
                        key={path}
                        to={path}
                        end
                        className={({ isActive }) =>
                            `sidebar-link${isActive ? " active" : ""}`
                        }
                    >
                        {label}
                    </NavLink>
                ))}
            </nav>

            <button
                type="button"
                className="sidebar-logout"
                onClick={logout}
            >
                Sair
            </button>
        </aside>
    );
}

export default Sidebar;