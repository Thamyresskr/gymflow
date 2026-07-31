/**
 * Componente responsável por proteger as rotas privadas.
 *
 * Responsabilidades:
 * - Aguardar a validação da sessão.
 * - Permitir acesso apenas para usuários autenticados.
 * - Preparar suporte para controle de acesso por perfis.
 */

import PropTypes from "prop-types";
import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useAuthContext } from "@/contexts/AuthContext";

/**
 * Caminho da tela de login.
 */
const LOGIN_ROUTE = "/login";

/**
 * Rota protegida.
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

    /**
     * Aguarda a validação da sessão.
     */
    if (loading) {
        return null;
    }

    /**
     * Usuário não autenticado.
     */
    if (!isAuthenticated) {
        return (
            <Navigate
                replace
                to={LOGIN_ROUTE}
                state={{
                    from: location,
                }}
            />
        );
    }

    /**
     * Controle de acesso por perfil.
     *
     * Será utilizado nas próximas sprints.
     */
    if (
        roles &&
        roles.length > 0 &&
        !roles.includes(user?.role)
    ) {
        return (
            <Navigate
                replace
                to="/"
            />
        );
    }

    return <Outlet />;
}

ProtectedRoute.propTypes = {
    roles: PropTypes.arrayOf(PropTypes.string),
};

ProtectedRoute.defaultProps = {
    roles: undefined,
};

export default ProtectedRoute;