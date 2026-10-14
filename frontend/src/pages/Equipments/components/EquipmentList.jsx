/**
 * Tabela de equipamentos.
 *
 * Responsabilidades:
 * - Exibir a lista de equipamentos.
 * - Permitir edição e exclusão somente quando autorizadas.
 */

import PropTypes from "prop-types";

import EmptyState from "@/components/ui/EmptyState/EmptyState";

import styles from "../Equipments.module.css";

function EquipmentList({
    equipments,
    onEdit,
    onDelete,
}) {
    const canManageEquipments =
        typeof onEdit === "function" &&
        typeof onDelete === "function";

    if (!equipments.length) {
        return (
            <EmptyState
                title="Nenhum equipamento encontrado"
                description={
                    canManageEquipments
                        ? "Cadastre um novo equipamento para começar."
                        : "Não há equipamentos para exibir."
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
                        <th>Categoria</th>
                        <th>Fabricante</th>
                        <th>Modelo</th>
                        <th>Patrimônio</th>
                        <th>Nº Série</th>
                        <th>Status</th>

                        {canManageEquipments && (
                            <th>Ações</th>
                        )}
                    </tr>
                </thead>

                <tbody>
                    {equipments.map((equipment) => (
                        <tr key={equipment.id}>
                            <td>{equipment.nome}</td>
                            <td>{equipment.categoria}</td>
                            <td>{equipment.fabricante}</td>
                            <td>{equipment.modelo}</td>
                            <td>{equipment.patrimonio}</td>
                            <td>{equipment.numero_serie}</td>

                            <td>
                                {equipment.status === "ativo"
                                    ? "Ativo"
                                    : equipment.status === "manutencao"
                                        ? "Manutenção"
                                        : equipment.status}
                            </td>

                            {canManageEquipments && (
                                <td className={styles.actions}>
                                    <button
                                        type="button"
                                        className={styles.editButton}
                                        onClick={() =>
                                            onEdit(equipment)
                                        }
                                        aria-label={`Editar equipamento ${equipment.nome}`}
                                    >
                                        Editar
                                    </button>

                                    <button
                                        type="button"
                                        className={styles.deleteButton}
                                        onClick={() =>
                                            onDelete(equipment)
                                        }
                                        aria-label={`Excluir equipamento ${equipment.nome}`}
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

EquipmentList.propTypes = {
    equipments: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.number.isRequired,
            nome: PropTypes.string.isRequired,
            categoria: PropTypes.string.isRequired,
            fabricante: PropTypes.string.isRequired,
            modelo: PropTypes.string.isRequired,
            patrimonio: PropTypes.string.isRequired,
            numero_serie: PropTypes.string.isRequired,
            observacao: PropTypes.string,
            status: PropTypes.string.isRequired,
        }),
    ).isRequired,

    onEdit: PropTypes.func,
    onDelete: PropTypes.func,
};

EquipmentList.defaultProps = {
    onEdit: undefined,
    onDelete: undefined,
};

export default EquipmentList;