/**
 * Instância centralizada do Axios.
 *
 * Responsabilidades:
 * - Configurar a URL base da API.
 * - Definir cabeçalhos padrão.
 * - Enviar automaticamente o JWT.
 * - Centralizar o tratamento de respostas.
 */

import axios from "axios";

/**
 * Chaves utilizadas no armazenamento local.
 */
const STORAGE_KEYS = Object.freeze({
    TOKEN: "gymflow_token",
});

/**
 * Instância compartilhada do Axios.
 */
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 15000,
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
    },
});

/**
 * Adiciona automaticamente o token JWT às requisições.
 */
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(STORAGE_KEYS.TOKEN);

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error),
);

/**
 * Intercepta respostas da API.
 */
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem(STORAGE_KEYS.TOKEN);

            /**
             * Futuramente poderemos redirecionar para a tela de login
             * ou disparar um evento global de logout.
             */
        }

        return Promise.reject(error);
    },
);

export default api;