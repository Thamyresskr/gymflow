
/**
 * Componente responsável por proteger as rotas privadas do GymFlow.
 *
 * Responsabilidades:
 * - Aguardar a validação da sessão.
 * - Permitir acesso somente a usuários autenticados.
 * - Controlar o acesso conforme o perfil do usuário.
 * - Aceitar o perfil recebido em `tipo` ou `role`.
 * - Redirecionar usuários sem permissão para o Dashboard.
 * - Preservar a rota original para redirecionamento após o login.
 */

import PropTypes from "prop-types";
import {
    Navigate,
    Outlet,
    useLocation,
} from "react-router-dom";

import { useAuthContext } from "@/contexts/AuthContext";

import { ROUTES } from "@/constants/routes";
import { USER_ROLES } from "@/constants/roles";

/**
 * Normaliza o perfil do usuário.
 *
 * O backend pode retornar o perfil em `tipo`,
 * enquanto algumas partes do frontend utilizam `role`.
 *
 * @param {Object|null} user
 * @returns {string}
 */
function getUserRole(user) {
    return String(
        user?.tipo ?? user?.role ?? "",
    ).trim().toUpperCase();
}

/**
 * Verifica se o usuário possui um dos perfis autorizados.
 *
 * @param {string[]} roles
 * @param {string} userRole
 * @returns {boolean}
 */
function hasPermission(roles, userRole) {
    if (!roles || roles.length === 0) {
        return true;
    }

    const allowedRoles = roles.map((role) =>
        String(role).trim().toUpperCase(),
    );

    return allowedRoles.includes(userRole);
}

/**
 * Rota protegida.
 *
 * Exemplos:
 *
 * <Route element={<ProtectedRoute />}>
 *     <Route path="/dashboard" element={<Dashboard />} />
 * </Route>
 *
 * <Route element={<ProtectedRoute roles={[USER_ROLES.ADMIN]} />}>
 *     <Route path="/users" element={<Users />} />
 * </Route>
 *
 * @param {Object} props
 * @param {string[]} [props.roles]
 */
function ProtectedRoute({ roles }) {
    const {
        loading,
        isAuthenticated,
        user,
    } = useAuthContext();

    const location = useLocation();

    // Aguarda a validação da sessão.
    if (loading) {
        return null;
    }

    // Usuário não autenticado: direciona para o login.
    if (!isAuthenticated) {
        return (
            <Navigate
                to={ROUTES.LOGIN}
                replace
                state={{
                    from: location,
                }}
            />
        );
    }

    const userRole = getUserRole(user);

    // Usuário autenticado, mas sem perfil autorizado.
    if (!hasPermission(roles, userRole)) {
        return (
            <Navigate
                to={ROUTES.DASHBOARD}
                replace
            />
        );
    }

    // Usuário autenticado e autorizado.
    return <Outlet />;
}

ProtectedRoute.propTypes = {
    roles: PropTypes.arrayOf(
        PropTypes.oneOf(Object.values(USER_ROLES)),
    ),
};

ProtectedRoute.defaultProps = {
    roles: undefined,
};

export default ProtectedRoute;
