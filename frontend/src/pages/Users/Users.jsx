/**
 * Página de gerenciamento de usuários.
 *
 * Responsabilidades:
 * - Listar usuários.
 * - Permitir pesquisa.
 * - Controlar o carregamento dos dados.
 * - Disponibilizar cadastro, edição e exclusão.
 * - Integrar com a API.
 */

import { useCallback, useEffect, useMemo, useState } from "react";

import ConfirmDialog from "@/components/ui/ConfirmDialog/ConfirmDialog";
import Loading from "@/components/ui/Loading/Loading";
import { MESSAGES } from "@/constants/messages";
import {
    notifyError,
    notifySuccess,
} from "@/services/notificationService";
import {
    createUser,
    deleteUser,
    listUsers,
    updateUser,
} from "@/services/userService";

import UserModal from "./components/UserModal";
import UserList from "./components/UserList";
import styles from "./Users.module.css";

function Users() {
    const [users, setUsers] = useState([]);
    const [search, setSearch] = useState("");
    const [loading, setLoading] = useState(true);

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const [loadingSave, setLoadingSave] = useState(false);

    const [isDeleteOpen, setIsDeleteOpen] = useState(false);
    const [userToDelete, setUserToDelete] = useState(null);
    const [loadingDelete, setLoadingDelete] = useState(false);

    /**
     * Carrega os usuários da API.
     */
    const loadUsers = useCallback(async () => {
        try {
            setLoading(true);

            const data = await listUsers();

            setUsers(data);
        } catch (error) {
            notifyError(
                error.response?.data?.detail ??
                    MESSAGES.USERS_ERROR,
            );
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadUsers();
    }, [loadUsers]);

    /**
     * Usuários filtrados conforme pesquisa.
     */
    const filteredUsers = useMemo(() => {
        const term = search.trim().toLowerCase();

        if (!term) return users;

        return users.filter(({ nome, email }) => {
            return (
                nome.toLowerCase().includes(term) ||
                email.toLowerCase().includes(term)
            );
        });
    }, [users, search]);

    /**
     * Novo usuário.
     */
    function handleNewUser() {
        setSelectedUser(null);
        setIsModalOpen(true);
    }

    /**
     * Editar usuário.
     *
     * @param {Object} user
     */
    function handleEdit(user) {
        setSelectedUser(user);
        setIsModalOpen(true);
    }

    /**
     * Fecha o modal.
     */
    function handleCloseModal() {
        setSelectedUser(null);
        setIsModalOpen(false);
    }

    /**
     * Salva um usuário.
     *
     * @param {Object} form
     */
    async function handleSaveUser(form) {
        try {
            setLoadingSave(true);

            if (selectedUser) {
                await updateUser(selectedUser.id, form);

                notifySuccess("Usuário atualizado com sucesso.");
            } else {
                await createUser(form);

                notifySuccess("Usuário cadastrado com sucesso.");
            }

            await loadUsers();

            handleCloseModal();
        } catch (error) {
            notifyError(
                error.response?.data?.detail ??
                    "Erro ao salvar usuário.",
            );
        } finally {
            setLoadingSave(false);
        }
    }

    /**
     * Solicita confirmação para exclusão.
     *
     * @param {Object} user
     */
    function handleDelete(user) {
        setUserToDelete(user);
        setIsDeleteOpen(true);
    }

    /**
     * Fecha o diálogo de exclusão.
     */
    function handleCloseDelete() {
        setUserToDelete(null);
        setIsDeleteOpen(false);
    }

    /**
     * Confirma exclusão.
     */
    async function handleConfirmDelete() {
        if (!userToDelete) return;

        try {
            setLoadingDelete(true);

            await deleteUser(userToDelete.id);

            notifySuccess("Usuário excluído com sucesso.");

            await loadUsers();

            handleCloseDelete();
        } catch (error) {
            notifyError(
                error.response?.data?.detail ??
                    "Erro ao excluir usuário.",
            );
        } finally {
            setLoadingDelete(false);
        }
    }

    if (loading) {
        return (
            <Loading
                fullScreen
                text="Carregando usuários..."
            />
        );
    }

    return (
        <section className={styles.container}>
            <header className={styles.header}>
                <div>
                    <h1>Usuários</h1>

                    <p>
                        Gerencie os usuários cadastrados
                        no sistema.
                    </p>
                </div>

                <button
                    type="button"
                    className={styles.addButton}
                    onClick={handleNewUser}
                >
                    Novo Usuário
                </button>
            </header>

            <section className={styles.toolbar}>
                <input
                    type="search"
                    className={styles.search}
                    placeholder="Pesquisar usuário..."
                    value={search}
                    onChange={(event) =>
                        setSearch(event.target.value)
                    }
                />
            </section>

            <UserList
                users={filteredUsers}
                onEdit={handleEdit}
                onDelete={handleDelete}
            />

            <UserModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                onSave={handleSaveUser}
                user={selectedUser}
                loading={loadingSave}
            />

            <ConfirmDialog
                isOpen={isDeleteOpen}
                title="Excluir usuário"
                message={
                    userToDelete
                        ? `Deseja realmente excluir o usuário "${userToDelete.nome}"?`
                        : ""
                }
                confirmText="Excluir"
                cancelText="Cancelar"
                loading={loadingDelete}
                onConfirm={handleConfirmDelete}
                onCancel={handleCloseDelete}
            />
        </section>
    );
}

export default Users;