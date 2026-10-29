
/**
 * Serviço responsável pelas operações de usuários do GymFlow.
 *
 * Responsabilidades:
 * - Listar usuários (ADMIN).
 * - Buscar usuário por ID (ADMIN).
 * - Cadastrar usuário pelo fluxo público.
 * - Cadastrar aluno pela RECEPÇÃO.
 * - Criar usuários por perfil (ADMIN).
 * - Atualizar e excluir usuários (ADMIN).
 */

import api from "@/services/api";

/**
 * Lista todos os usuários cadastrados.
 *
 * Requer permissão ADMIN.
 *
 * @returns {Promise<Array>}
 */
export async function listUsers() {
    const { data } = await api.get("/users/");
    return data;
}

/**
 * Busca um usuário pelo identificador.
 *
 * Requer permissão ADMIN.
 *
 * @param {number} id
 * @returns {Promise<Object>}
 */
export async function getUser(id) {
    const { data } = await api.get(`/users/${id}`);
    return data;
}

/**
 * Cadastra um aluno pelo fluxo público.
 * O backend define o perfil como ALUNO.
 *
 * @param {Object} user
 * @returns {Promise<Object>}
 */
export async function createUser(user) {
    const { data } = await api.post("/users/", user);
    return data;
}

/**
 * Cadastra exclusivamente um aluno pela RECEPÇÃO.
 *
 * Requer autenticação com perfil RECEPCAO.
 * O perfil é definido pelo backend, não pelo frontend.
 *
 * @param {Object} student
 * @returns {Promise<Object>}
 */
export async function createReceptionStudent(student) {
    const { data } = await api.post(
        "/users/reception",
        student,
    );

    return data;
}

/**
 * Cria um usuário com o perfil informado.
 *
 * Requer permissão ADMIN.
 *
 * @param {Object} user
 * @returns {Promise<Object>}
 */
export async function createAdminUser(user) {
    const { data } = await api.post("/users/admin", user);
    return data;
}

/**
 * Atualiza um usuário.
 *
 * Requer permissão ADMIN.
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
 * Requer permissão ADMIN.
 *
 * @param {number} id
 * @returns {Promise<void>}
 */
export async function deleteUser(id) {
    await api.delete(`/users/${id}`);
}
