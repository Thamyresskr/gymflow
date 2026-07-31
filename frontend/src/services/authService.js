/**
 * Serviços relacionados à autenticação.
 *
 * Responsabilidades:
 * - Realizar login.
 * - Armazenar o token JWT.
 * - Recuperar o token.
 * - Recuperar o usuário autenticado.
 * - Encerrar sessão.
 * - Fornecer o cabeçalho Authorization.
 */

import api from "@/services/api";

/**
 * Chaves utilizadas no armazenamento local.
 */
const STORAGE_KEYS = Object.freeze({
    TOKEN: "gymflow_token",
});

/**
 * Armazena o token JWT.
 *
 * @param {string} token
 */
function saveToken(token) {
    localStorage.setItem(STORAGE_KEYS.TOKEN, token);
}

/**
 * Remove o token armazenado.
 */
function removeToken() {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
}

/**
 * Realiza o login do usuário.
 *
 * @param {string} email
 * @param {string} password
 * @returns {Promise<Object>}
 */
export async function login(email, password) {
    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    try {
        const response = await api.post("/auth/login", formData, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        const token = response.data?.access_token;

        if (!token) {
            throw new Error("Token de autenticação não retornado pela API.");
        }

        saveToken(token);

        return response.data;
    } catch (error) {
        removeToken();
        throw error;
    }
}

/**
 * Retorna os dados do usuário autenticado.
 *
 * @returns {Promise<Object>}
 */
export async function getCurrentUser() {
    const response = await api.get("/users/me", {
        headers: getAuthorizationHeader(),
    });

    return response.data;
}

/**
 * Encerra a sessão do usuário.
 */
export function logout() {
    removeToken();
}

/**
 * Retorna o token JWT armazenado.
 *
 * @returns {string|null}
 */
export function getToken() {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
}

/**
 * Verifica se existe um usuário autenticado.
 *
 * @returns {boolean}
 */
export function isAuthenticated() {
    return Boolean(getToken());
}

/**
 * Retorna o cabeçalho Authorization.
 *
 * @returns {Object}
 */
export function getAuthorizationHeader() {
    const token = getToken();

    return token
        ? {
              Authorization: `Bearer ${token}`,
          }
        : {};
}