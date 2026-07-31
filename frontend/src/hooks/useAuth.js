/**
 * Hook personalizado para acesso ao contexto de autenticação.
 *
 * Centraliza o acesso ao AuthContext, evitando que os componentes
 * importem diretamente o contexto da aplicação.
 */

import { useAuthContext } from "@/contexts/AuthContext";

/**
 * Retorna o contexto de autenticação da aplicação.
 *
 * @returns {Object}
 */
export function useAuth() {
    return useAuthContext();
}