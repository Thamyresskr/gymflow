/**
 * Barra lateral de navegação da aplicação.
 */

import { NavLink } from "react-router-dom";

import { useAuthContext } from "@/contexts/AuthContext";
import { ROUTES } from "@/constants/routes";

import "./Sidebar.css";

const MENU_ITEMS = [
    {
        label: "Dashboard",
        path: ROUTES.DASHBOARD,
        roles: ["ADMIN", "PROFESSOR", "ALUNO"],
    },
    {
        label: "Check-ins",
        path: ROUTES.CHECKINS,
        roles: ["ADMIN", "PROFESSOR", "ALUNO"],
    },
    {
        label: "Equipamentos",
        path: ROUTES.EQUIPMENTS,
        roles: ["ADMIN", "PROFESSOR"],
    },
    {
        label: "Usuários",
        path: ROUTES.USERS,
        roles: ["ADMIN"],
    },
];

function Sidebar() {
    const { user, logout } = useAuthContext();

    const userRole = (
        user?.tipo ?? user?.role ?? ""
    ).toUpperCase();

    const menu = MENU_ITEMS.filter((item) =>
        item.roles.includes(userRole)
    );

    return (
        <aside
            className="sidebar"
            aria-label="Barra lateral"
        >
            <div className="sidebar-logo">
                <h2>GymFlow</h2>
            </div>

            <div className="sidebar-user">
                <strong>{user?.nome ?? "Usuário"}</strong>
                <span>{user?.tipo ?? user?.role ?? ""}</span>
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