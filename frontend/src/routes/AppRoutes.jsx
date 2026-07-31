/**
 * Configuração das rotas da aplicação GymFlow.
 *
 * Estrutura:
 * - Rotas públicas.
 * - Rotas protegidas.
 * - Layout principal.
 * - Redirecionamentos.
 */

import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import MainLayout from "@/layouts/MainLayout";

import Checkins from "@/pages/Checkins/Checkins";
import Dashboard from "@/pages/Dashboard/Dashboard";
import Login from "@/pages/Login/Login";
import Users from "@/pages/Users/Users";

/**
 * Caminhos das rotas da aplicação.
 */
export const ROUTES = Object.freeze({
    ROOT: "/",
    LOGIN: "/login",
    DASHBOARD: "/dashboard",
    USERS: "/users",
    CHECKINS: "/checkins",
});

/**
 * Componente responsável pelo roteamento da aplicação.
 */
function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>

                {/* Página inicial */}
                <Route
                    path={ROUTES.ROOT}
                    element={
                        <Navigate
                            to={ROUTES.DASHBOARD}
                            replace
                        />
                    }
                />

                {/* Rotas públicas */}
                <Route
                    path={ROUTES.LOGIN}
                    element={<Login />}
                />

                {/* Rotas protegidas */}
                <Route element={<ProtectedRoute />}>
                    <Route element={<MainLayout />}>
                        <Route
                            path={ROUTES.DASHBOARD}
                            element={<Dashboard />}
                        />

                        <Route
                            path={ROUTES.USERS}
                            element={<Users />}
                        />

                        <Route
                            path={ROUTES.CHECKINS}
                            element={<Checkins />}
                        />
                    </Route>
                </Route>

                {/* Página não encontrada */}
                <Route
                    path="*"
                    element={
                        <Navigate
                            to={ROUTES.DASHBOARD}
                            replace
                        />
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default AppRoutes;