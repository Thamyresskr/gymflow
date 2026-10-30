
/**
 * Barra lateral de navegação da aplicação GymFlow.
 */

import { NavLink } from "react-router-dom";

import { useAuthContext } from "@/contexts/AuthContext";
import { ROUTES } from "@/constants/routes";
import { USER_ROLES } from "@/constants/roles";

import "./Sidebar.css";

const MENU_ITEMS = [
    {
        label: "Dashboard",
        path: ROUTES.DASHBOARD,
        roles: Object.values(USER_ROLES),
    },
    {
        label: "Check-ins",
        path: ROUTES.CHECKINS,
        roles: Object.values(USER_ROLES),
    },
    {
        label: "Equipamentos",
        path: ROUTES.EQUIPMENTS,
        roles: [
            USER_ROLES.ADMIN,
            USER_ROLES.PROFESSOR,
            USER_ROLES.RECEPCAO,
        ],
    },
    {
        label: "Cadastro de Alunos",
        path: ROUTES.STUDENT_REGISTRATION,
        roles: [USER_ROLES.RECEPCAO],
    },
    {
        label: "Usuários",
        path: ROUTES.USERS,
        roles: [USER_ROLES.ADMIN],
    },
];

function Sidebar() {
    const { user, logout } = useAuthContext();

    const userRole = String(
        user?.tipo ?? user?.role ?? "",
    ).trim().toUpperCase();

    const displayName = user?.nome?.trim() || "Usuário";

    const menu = MENU_ITEMS.filter((item) =>
        item.roles.includes(userRole),
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
                <strong
                    className="sidebar-user-name"
                    title={displayName}
                >
                    {displayName}
                </strong>

                <span className="sidebar-user-role">
                    {userRole}
                </span>
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
