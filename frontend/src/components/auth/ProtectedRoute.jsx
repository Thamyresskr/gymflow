import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth";

/**
 * Protege as rotas privadas da aplicação.
 *
 * Caso o usuário não esteja autenticado,
 * ele será redirecionado para a tela de login.
 */
function ProtectedRoute() {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return (
            <Navigate
                to="/login"
                replace
            />
        );
    }

    return <Outlet />;
}

export default ProtectedRoute;