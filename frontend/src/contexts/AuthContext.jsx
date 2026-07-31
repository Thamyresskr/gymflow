/**
 * Contexto global de autenticação.
 *
 * Responsabilidades:
 * - Controlar o estado de autenticação.
 * - Armazenar o usuário autenticado.
 * - Disponibilizar login, logout e atualização do usuário.
 * - Compartilhar o estado entre todos os componentes.
 */

import PropTypes from "prop-types";
import {
    createContext,
    useContext,
    useEffect,
    useMemo,
    useState,
} from "react";

import * as authService from "@/services/authService";

/**
 * Contexto de autenticação.
 */
const AuthContext = createContext(null);

/**
 * Provider responsável por disponibilizar o contexto de autenticação.
 */
export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);

    const [loading, setLoading] = useState(true);

    const [isAuthenticated, setIsAuthenticated] = useState(false);

    /**
     * Carrega os dados do usuário autenticado.
     */
    async function loadUser() {
        try {
            const currentUser = await authService.getCurrentUser();

            setUser(currentUser);
            setIsAuthenticated(true);
        } catch (error) {
            authService.logout();

            setUser(null);
            setIsAuthenticated(false);
        } finally {
            setLoading(false);
        }
    }

    /**
     * Verifica se existe uma sessão válida ao iniciar a aplicação.
     */
    useEffect(() => {
        if (authService.isAuthenticated()) {
            loadUser();
        } else {
            setLoading(false);
        }
    }, []);

    /**
     * Realiza o login.
     *
     * @param {string} email
     * @param {string} password
     */
    async function login(email, password) {
        await authService.login(email, password);

        await loadUser();
    }

    /**
     * Atualiza os dados do usuário autenticado.
     */
    async function refreshUser() {
        await loadUser();
    }

    /**
     * Encerra a sessão.
     */
    function logout() {
        authService.logout();

        setUser(null);
        setIsAuthenticated(false);
    }

    /**
     * Valor compartilhado pelo contexto.
     */
    const value = useMemo(
        () => ({
            user,
            loading,
            isAuthenticated,
            login,
            logout,
            refreshUser,
        }),
        [
            user,
            loading,
            isAuthenticated,
        ],
    );

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

AuthProvider.propTypes = {
    children: PropTypes.node.isRequired,
};

/**
 * Hook para acesso ao contexto de autenticação.
 *
 * @returns {Object}
 */
export function useAuthContext() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error(
            "useAuthContext deve ser utilizado dentro de um AuthProvider.",
        );
    }

    return context;
}