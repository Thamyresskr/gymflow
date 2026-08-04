/**
 * Configuração das rotas da aplicação GymFlow.
 *
 * Responsabilidades:
 * - Definir todas as rotas.
 * - Separar páginas públicas e privadas.
 * - Aplicar layouts.
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

import { ROUTES } from "@/constants/routes";

import Dashboard from "@/pages/Dashboard/Dashboard";
import Users from "@/pages/Users/Users";
import Checkins from "@/pages/Checkins/Checkins";
import Login from "@/pages/Login/Login";

function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>

                <Route
                    path={ROUTES.ROOT}
                    element={
                        <Navigate
                            to={ROUTES.DASHBOARD}
                            replace
                        />
                    }
                />

                <Route
                    path={ROUTES.LOGIN}
                    element={<Login />}
                />

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