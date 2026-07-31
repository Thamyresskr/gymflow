/**
 * Serviço responsável pelas operações de usuários.
 *
 * Responsabilidades:
 * - Listar usuários.
 * - Buscar usuário por ID.
 * - Cadastrar usuário.
 * - Atualizar usuário.
 * - Excluir usuário.
 */

import api from "@/services/api";

/**
 * Lista todos os usuários.
 *
 * @returns {Promise<Array>}
 */
export async function listUsers() {
    const { data } = await api.get("/users");
    return data;
}

/**
 * Busca um usuário pelo identificador.
 *
 * @param {number} id
 * @returns {Promise<Object>}
 */
export async function getUser(id) {
    const { data } = await api.get(`/users/${id}`);
    return data;
}

/**
 * Cadastra um novo usuário.
 *
 * @param {Object} user
 * @returns {Promise<Object>}
 */
export async function createUser(user) {
    const { data } = await api.post("/users", user);
    return data;
}

/**
 * Atualiza um usuário.
 *
 * @param {number} id
 * @param {Object} user
 * @returns {Promise<Object>}
 */
export async function updateUser(id, user) {
    const { data } = await api.put(`/users/${id}`, user);
    return data;
}

/**
 * Remove um usuário.
 *
 * @param {number} id
 * @returns {Promise<void>}
 */
export async function deleteUser(id) {
    await api.delete(`/users/${id}`);
}