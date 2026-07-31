/**
 * Tabela de usuários.
 *
 * Responsabilidades:
 * - Exibir a lista de usuários.
 * - Acionar edição.
 * - Acionar exclusão.
 */

import PropTypes from "prop-types";

import EmptyState from "@/components/ui/EmptyState/EmptyState";

import styles from "../Users.module.css";

function UserList({
    users,
    onEdit,
    onDelete,
}) {
    if (!users.length) {
        return (
            <EmptyState
                title="Nenhum usuário encontrado"
                description="Cadastre um novo usuário para começar."
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
                        <th>Ações</th>
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
                                {user.ativo
                                    ? "Ativo"
                                    : "Inativo"}
                            </td>

                            <td className={styles.actions}>
                                <button
                                    type="button"
                                    className={styles.editButton}
                                    onClick={() => onEdit(user)}
                                >
                                    Editar
                                </button>

                                <button
                                    type="button"
                                    className={styles.deleteButton}
                                    onClick={() => onDelete(user)}
                                >
                                    Excluir
                                </button>
                            </td>
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
    onEdit: PropTypes.func.isRequired,
    onDelete: PropTypes.func.isRequired,
};

export default UserList;