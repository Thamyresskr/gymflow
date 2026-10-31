
/**
 * Configuração das rotas da aplicação GymFlow.
 *
 * Responsabilidades:
 * - Definir rotas públicas e privadas.
 * - Aplicar layouts.
 * - Controlar permissões por perfil.
 * - Gerenciar redirecionamentos.
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
import { USER_ROLES } from "@/constants/roles";

import Dashboard from "@/pages/Dashboard/Dashboard";
import Users from "@/pages/Users/Users";
import Equipments from "@/pages/Equipments/Equipments";
import Checkins from "@/pages/Checkins/Checkins";
import Login from "@/pages/Login/Login";
import StudentRegistration from "@/pages/StudentRegistration/StudentRegistration";

function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Rota inicial */}
                <Route
                    path={ROUTES.ROOT}
                    element={
                        <Navigate
                            to={ROUTES.DASHBOARD}
                            replace
                        />
                    }
                />

                {/* Rota pública */}
                <Route
                    path={ROUTES.LOGIN}
                    element={<Login />}
                />

                {/* Rotas privadas: exigem autenticação */}
                <Route element={<ProtectedRoute />}>
                    <Route element={<MainLayout />}>

                        {/* Dashboard: todos os perfis autenticados */}
                        <Route
                            path={ROUTES.DASHBOARD}
                            element={<Dashboard />}
                        />

                        {/* Check-ins: todos os perfis autenticados */}
                        <Route
                            path={ROUTES.CHECKINS}
                            element={<Checkins />}
                        />

                        {/* Equipamentos: ADMIN, RECEPCAO e PROFESSOR */}
                        <Route
                            element={
                                <ProtectedRoute
                                    roles={[
                                        USER_ROLES.ADMIN,
                                        USER_ROLES.RECEPCAO,
                                        USER_ROLES.PROFESSOR,
                                    ]}
                                />
                            }
                        >
                            <Route
                                path={ROUTES.EQUIPMENTS}
                                element={<Equipments />}
                            />
                        </Route>

                        {/* Usuários: acesso exclusivo do ADMIN */}
                        <Route
                            element={
                                <ProtectedRoute
                                    roles={[USER_ROLES.ADMIN]}
                                />
                            }
                        >
                            <Route
                                path={ROUTES.USERS}
                                element={<Users />}
                            />
                        </Route>

                        {/* Cadastro de alunos: acesso exclusivo da RECEPÇÃO */}
                        <Route
                            element={
                                <ProtectedRoute
                                    roles={[USER_ROLES.RECEPCAO]}
                                />
                            }
                        >
                            <Route
                                path={ROUTES.STUDENT_REGISTRATION}
                                element={<StudentRegistration />}
                            />
                        </Route>

                    </Route>
                </Route>

                {/* Rota não encontrada */}
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
