/**
 * Tabela de usuários.
 *
 * Responsabilidades:
 * - Exibir a lista de usuários.
 * - Permitir edição e exclusão somente quando autorizadas.
 */

import PropTypes from "prop-types";

import EmptyState from "@/components/ui/EmptyState/EmptyState";

import styles from "../Users.module.css";

function UserList({
    users,
    onEdit,
    onDelete,
}) {
    const canManageUsers =
        typeof onEdit === "function" &&
        typeof onDelete === "function";

    if (!users.length) {
        return (
            <EmptyState
                title="Nenhum usuário encontrado"
                description={
                    canManageUsers
                        ? "Cadastre um novo usuário para começar."
                        : "Não há usuários para exibir."
                }
            />
        );
    }

    return (
        <section className={styles.tableContainer}>
            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>E-mail</th>
                        <th>Telefone</th>
                        <th>Matrícula</th>
                        <th>Perfil</th>
                        <th>Status</th>

                        {canManageUsers && <th>Ações</th>}
                    </tr>
                </thead>

                <tbody>
                    {users.map((user) => (
                        <tr key={user.id}>
                            <td>{user.nome}</td>
                            <td>{user.email}</td>
                            <td>{user.telefone ?? "-"}</td>
                            <td>{user.matricula ?? "-"}</td>
                            <td>{user.tipo}</td>

                            <td>
                                {user.ativo ? "Ativo" : "Inativo"}
                            </td>

                            {canManageUsers && (
                                <td className={styles.actions}>
                                    <button
                                        type="button"
                                        className={styles.editButton}
                                        onClick={() => onEdit(user)}
                                        aria-label={`Editar usuário ${user.nome}`}
                                    >
                                        Editar
                                    </button>

                                    <button
                                        type="button"
                                        className={styles.deleteButton}
                                        onClick={() => onDelete(user)}
                                        aria-label={`Excluir usuário ${user.nome}`}
                                    >
                                        Excluir
                                    </button>
                                </td>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>
        </section>
    );
}

UserList.propTypes = {
    users: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.number.isRequired,
            nome: PropTypes.string.isRequired,
            email: PropTypes.string.isRequired,
            telefone: PropTypes.string,
            matricula: PropTypes.string,
            tipo: PropTypes.string.isRequired,
            ativo: PropTypes.bool.isRequired,
        }),
    ).isRequired,
    onEdit: PropTypes.func,
    onDelete: PropTypes.func,
};

UserList.defaultProps = {
    onEdit: undefined,
    onDelete: undefined,
};

export default UserList;