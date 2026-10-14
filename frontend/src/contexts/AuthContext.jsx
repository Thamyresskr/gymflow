
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
    useCallback,
    useContext,
    useEffect,
    useMemo,
    useState,
} from "react";

import * as authService from "@/services/authService";

const AuthContext = createContext(null);

/**
 * Provider responsável por disponibilizar o contexto.
 */
export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(
        () => authService.isAuthenticated(),
    );
    const [isAuthenticated, setIsAuthenticated] = useState(
        () => authService.isAuthenticated(),
    );

    /**
     * Busca o usuário autenticado e normaliza seu perfil.
     * isActive impede atualizações após a limpeza do efeito.
     */
    const loadUser = useCallback(async (isActive = () => true) => {
        try {
            const currentUser = await authService.getCurrentUser();

            if (!currentUser) {
                throw new Error(
                    "A API não retornou os dados do usuário.",
                );
            }

            const normalizedUser = {
                ...currentUser,
                role: String(
                    currentUser.tipo ?? currentUser.role ?? "",
                ).toUpperCase(),
            };

            if (isActive()) {
                setUser(normalizedUser);
                setIsAuthenticated(true);
            }

            return normalizedUser;
        } catch {
            if (isActive()) {
                authService.logout();
                setUser(null);
                setIsAuthenticated(false);
            }

            return null;
        } finally {
            if (isActive()) {
                setLoading(false);
            }
        }
    }, []);

    /**
     * Valida uma sessão existente na inicialização.
     */
    useEffect(() => {
        let active = true;

        async function initializeSession() {
            if (!authService.isAuthenticated()) {
                return;
            }

            await loadUser(() => active);
        }

        void initializeSession();

        return () => {
            active = false;
        };
    }, [loadUser]);

    /**
     * Realiza o login e carrega os dados do usuário.
     */
    const login = useCallback(async (email, password) => {
        setLoading(true);

        try {
            await authService.login(email, password);

            const currentUser = await loadUser();

            if (!currentUser) {
                throw new Error(
                    "Não foi possível carregar os dados do usuário após o login.",
                );
            }

            return currentUser;
        } catch (error) {
            authService.logout();
            setUser(null);
            setIsAuthenticated(false);
            throw error;
        } finally {
            setLoading(false);
        }
    }, [loadUser]);

    /**
     * Atualiza os dados do usuário autenticado.
     */
    const refreshUser = useCallback(
        () => loadUser(),
        [loadUser],
    );

    /**
     * Encerra a sessão local.
     */
    const logout = useCallback(() => {
        authService.logout();
        setUser(null);
        setIsAuthenticated(false);
        setLoading(false);
    }, []);

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
            login,
            logout,
            refreshUser,
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
 * Hook para acessar o contexto de autenticação.
 */
 // eslint-disable-next-line react-refresh/only-export-components
export function useAuthContext() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error(
            "useAuthContext deve ser utilizado dentro de um AuthProvider.",
        );
    }

    return context;
}
