/**
 * Modal de cadastro e edição de usuários.
 *
 * Responsabilidades:
 * - Cadastrar usuários.
 * - Editar usuários.
 * - Reutilizar os componentes de UI.
 */

import { useState } from "react";
import PropTypes from "prop-types";

import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Modal from "@/components/ui/Modal/Modal";

import styles from "./UserModal.module.css";

const INITIAL_FORM = {
    nome: "",
    email: "",
    telefone: "",
    matricula: "",
    senha: "",
    ativo: true,
};

function buildInitialForm(user) {
    if (!user) {
        return { ...INITIAL_FORM };
    }

    return {
        nome: user.nome ?? "",
        email: user.email ?? "",
        telefone: user.telefone ?? "",
        matricula: user.matricula ?? "",
        senha: "",
        ativo: user.ativo ?? true,
    };
}

function buildPayload(form, isEditing) {
    return {
        nome: form.nome.trim(),
        email: form.email.trim(),
        telefone: form.telefone.trim() || null,
        matricula: form.matricula.trim() || null,
        ...(isEditing
            ? {
                  ativo: form.ativo,
              }
            : {
                  senha: form.senha,
              }),
    };
}

function UserModal({
    isOpen,
    onClose,
    onSave,
    user,
    loading,
}) {
    const [form, setForm] = useState(
        () => buildInitialForm(user),
    );

    function handleChange(event) {
        const {
            name,
            value,
            type,
            checked,
        } = event.target;

        setForm((previous) => ({
            ...previous,
            [name]:
                type === "checkbox"
                    ? checked
                    : value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();

        await onSave(
            buildPayload(form, Boolean(user)),
        );
    }

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title={
                user
                    ? "Editar Usuário"
                    : "Novo Usuário"
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
                    autoComplete="name"
                    minLength={3}
                    maxLength={100}
                />

                <Input
                    id="email"
                    name="email"
                    label="E-mail"
                    type="email"
                    value={form.email}
                    onChange={handleChange}
                    required
                    autoComplete="email"
                />

                <Input
                    id="telefone"
                    name="telefone"
                    label="Telefone"
                    value={form.telefone}
                    onChange={handleChange}
                    placeholder="(11) 99999-8888"
                    autoComplete="tel"
                />

                <Input
                    id="matricula"
                    name="matricula"
                    label="Matrícula"
                    value={form.matricula}
                    onChange={handleChange}
                />

                {!user && (
                    <Input
                        id="senha"
                        name="senha"
                        label="Senha"
                        type="password"
                        value={form.senha}
                        onChange={handleChange}
                        required
                        minLength={6}
                        placeholder="Mínimo 6 caracteres"
                        autoComplete="new-password"
                    />
                )}

                {user && (
                    <div className={styles.formGroup}>
                        <label className={styles.checkbox}>
                            <input
                                type="checkbox"
                                name="ativo"
                                checked={form.ativo}
                                onChange={handleChange}
                            />
                            Usuário ativo
                        </label>
                    </div>
                )}

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
                        {user
                            ? "Atualizar"
                            : "Cadastrar"}
                    </Button>
                </div>
            </form>
        </Modal>
    );
}

UserModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onSave: PropTypes.func.isRequired,
    loading: PropTypes.bool,
    user: PropTypes.shape({
        id: PropTypes.number,
        nome: PropTypes.string,
        email: PropTypes.string,
        telefone: PropTypes.string,
        matricula: PropTypes.string,
        ativo: PropTypes.bool,
    }),
};

UserModal.defaultProps = {
    loading: false,
    user: null,
};

export default UserModal;