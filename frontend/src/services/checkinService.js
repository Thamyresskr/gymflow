/**
 * Serviços relacionados aos check-ins.
 *
 * Responsabilidades:
 * - Consultar check-ins.
 * - Consultar check-ins do usuário autenticado.
 * - Consultar check-ins ativos.
 * - Registrar check-in.
 * - Registrar check-out.
 */

import api from "./api";

/**
 * Retorna o histórico completo de check-ins.
 *
 * Utilizado por perfis administrativos.
 *
 * @returns {Promise<Array>}
 */
export async function getCheckins() {
    const response = await api.get("/checkins/");

    return response.data;
}

/**
 * Retorna os check-ins do usuário autenticado.
 *
 * Utilizado pelo perfil ALUNO.
 *
 * @returns {Promise<Array>}
 */
export async function getMyCheckins() {
    const response = await api.get("/checkins/me");

    return response.data;
}

/**
 * Retorna todos os check-ins ativos.
 *
 * @returns {Promise<Array>}
 */
export async function getActiveCheckins() {
    const response = await api.get("/checkins/ativos");

    return response.data;
}

/**
 * Realiza um novo check-in.
 *
 * @returns {Promise<Object>}
 */
export async function registerCheckin() {
    const response = await api.post("/checkins/");

    return response.data;
}

/**
 * Realiza o check-out.
 *
 * @param {number} checkinId
 * @returns {Promise<Object>}
 */
export async function registerCheckout(checkinId) {
    const response = await api.put(
        `/checkins/${checkinId}/checkout`,
    );

    return response.data;
}

export default {
    getCheckins,
    getMyCheckins,
    getActiveCheckins,
    registerCheckin,
    registerCheckout,
};