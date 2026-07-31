/**
 * Serviços relacionados ao Dashboard.
 */

import api from "./api";

/**
 * Obtém os dados do dashboard.
 *
 * @returns {Promise<Object>}
 */
export async function getDashboard() {
    const response = await api.get("/dashboard/");
    return response.data;
}

export default {
    getDashboard,
};