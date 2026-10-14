/**
 * Serviços relacionados ao Dashboard.
 */

import api from "./api";

/**
 * Obtém os indicadores completos do Dashboard.
 * Permitido para ADMIN e RECEPCAO.
 *
 * @returns {Promise<Object>}
 */
export async function getDashboard() {
    const response = await api.get("/dashboard/");
    return response.data;
}

/**
 * Obtém somente a ocupação atual da academia.
 * Disponível para qualquer usuário autenticado.
 *
 * @returns {Promise<{ocupacao_atual: number}>}
 */
export async function getOcupacao() {
    const response = await api.get("/dashboard/ocupacao");
    return response.data;
}

export default {
    getDashboard,
    getOcupacao,
};
