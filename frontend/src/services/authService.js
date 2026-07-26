import api from "./api";

const TOKEN_KEY = "gymflow_token";

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

  const response = await api.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  localStorage.setItem(TOKEN_KEY, response.data.access_token);

  return response.data;
}

/**
 * Remove o token armazenado.
 */
export function logout() {
  localStorage.removeItem(TOKEN_KEY);
}

/**
 * Retorna o token JWT.
 *
 * @returns {string|null}
 */
export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Verifica se o usuário está autenticado.
 *
 * @returns {boolean}
 */
export function isAuthenticated() {
  return !!getToken();
}

/**
 * Retorna o cabeçalho Authorization para requisições autenticadas.
 *
 * @returns {Object}
 */
export function getAuthorizationHeader() {
  const token = getToken();

  if (!token) {
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
}