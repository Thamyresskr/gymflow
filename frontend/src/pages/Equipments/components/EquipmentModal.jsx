/**
 * Modal de cadastro e edição de equipamentos.
 *
 * Responsabilidades:
 * - Cadastrar equipamentos.
 * - Editar equipamentos.
 * - Reutilizar os componentes de UI.
 */

import { useState } from "react";
import PropTypes from "prop-types";

import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Modal from "@/components/ui/Modal/Modal";

import styles from "./EquipmentModal.module.css";

const INITIAL_FORM = {
    nome: "",
    categoria: "",
    fabricante: "",
    modelo: "",
    patrimonio: "",
    numero_serie: "",
    observacao: "",
    status: "ativo",
};

function buildPayload(form) {
    return {
        nome: form.nome.trim(),
        categoria: form.categoria.trim(),
        fabricante: form.fabricante.trim(),
        modelo: form.modelo.trim(),
        patrimonio: form.patrimonio.trim(),
        numero_serie: form.numero_serie.trim(),
        observacao: form.observacao.trim(),
        status: form.status,
    };
}

function buildInitialForm(equipment) {
    if (!equipment) {
        return { ...INITIAL_FORM };
    }

    return {
        nome: equipment.nome ?? "",
        categoria: equipment.categoria ?? "",
        fabricante: equipment.fabricante ?? "",
        modelo: equipment.modelo ?? "",
        patrimonio: equipment.patrimonio ?? "",
        numero_serie: equipment.numero_serie ?? "",
        observacao: equipment.observacao ?? "",
        status: equipment.status ?? "ativo",
    };
}

function EquipmentModal({
    isOpen,
    onClose,
    onSave,
    equipment,
    loading,
}) {
    const [form, setForm] = useState(
        () => buildInitialForm(equipment),
    );

    function handleChange(event) {
        const { name, value } = event.target;

        setForm((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();
        await onSave(buildPayload(form));
    }

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title={
                equipment
                    ? "Editar Equipamento"
                    : "Novo Equipamento"
            }
            width="720px"
        >
            <form
                className={styles.form}
                onSubmit={handleSubmit}
            >
                <Input
                    id="nome"
                    name="nome"
                    label="Nome"
                    value={form.nome}
                    onChange={handleChange}
                    required
                    autoFocus
                    minLength={2}
                    maxLength={100}
                />

                <div className={styles.formGroup}>
                    <label htmlFor="categoria">
                        Categoria
                    </label>

                    <select
                        id="categoria"
                        name="categoria"
                        value={form.categoria}
                        onChange={handleChange}
                        required
                        className={styles.select}
                    >
                        <option value="">
                            Selecione uma categoria
                        </option>
                        <option value="cardio">
                            Cardio
                        </option>
                        <option value="musculacao">
                            Musculação
                        </option>
                        <option value="funcional">
                            Funcional
                        </option>
                        <option value="outros">
                            Outros
                        </option>
                    </select>
                </div>

                <Input
                    id="fabricante"
                    name="fabricante"
                    label="Fabricante"
                    value={form.fabricante}
                    onChange={handleChange}
                    required
                    minLength={2}
                    maxLength={100}
                />

                <Input
                    id="modelo"
                    name="modelo"
                    label="Modelo"
                    value={form.modelo}
                    onChange={handleChange}
                    required
                    maxLength={100}
                />

                <Input
                    id="patrimonio"
                    name="patrimonio"
                    label="Patrimônio"
                    value={form.patrimonio}
                    onChange={handleChange}
                    required
                    maxLength={50}
                />

                <Input
                    id="numero_serie"
                    name="numero_serie"
                    label="Número de série"
                    value={form.numero_serie}
                    onChange={handleChange}
                    required
                    maxLength={100}
                />

                <div className={styles.formGroup}>
                    <label htmlFor="observacao">
                        Observação
                    </label>

                    <textarea
                        id="observacao"
                        name="observacao"
                        value={form.observacao}
                        onChange={handleChange}
                        maxLength={500}
                        rows={4}
                        className={styles.textarea}
                        placeholder="Digite uma observação, se necessário."
                    />
                </div>

                <div className={styles.formGroup}>
                    <label htmlFor="status">
                        Status
                    </label>

                    <select
                        id="status"
                        name="status"
                        value={form.status}
                        onChange={handleChange}
                        required
                        className={styles.select}
                    >
                        <option value="ativo">
                            Ativo
                        </option>
                        <option value="manutencao">
                            Manutenção
                        </option>
                    </select>
                </div>

                <div className={styles.actions}>
                    <Button
                        type="button"
                        variant="secondary"
                        onClick={onClose}
                        disabled={loading}
                    >
                        Cancelar
                    </Button>

                    <Button
                        type="submit"
                        variant="primary"
                        loading={loading}
                    >
                        {equipment
                            ? "Atualizar"
                            : "Cadastrar"}
                    </Button>
                </div>
            </form>
        </Modal>
    );
}

EquipmentModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onSave: PropTypes.func.isRequired,
    loading: PropTypes.bool,
    equipment: PropTypes.shape({
        id: PropTypes.number,
        nome: PropTypes.string,
        categoria: PropTypes.string,
        fabricante: PropTypes.string,
        modelo: PropTypes.string,
        patrimonio: PropTypes.string,
        numero_serie: PropTypes.string,
        observacao: PropTypes.string,
        status: PropTypes.string,
    }),
};

EquipmentModal.defaultProps = {
    loading: false,
    equipment: null,
};

export default EquipmentModal;