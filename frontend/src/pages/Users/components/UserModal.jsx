/**
 * Modal de cadastro e edição de usuários.
 *
 * Responsabilidades:
 * - Cadastrar usuários.
 * - Editar usuários.
 * - Validar o formulário.
 * - Reutilizar o Modal genérico.
 */

import { useEffect, useState } from "react";
import PropTypes from "prop-types";

import Modal from "@/components/ui/Modal/Modal";

const INITIAL_FORM = {
    nome: "",
    email: "",
    telefone: "",
    matricula: "",
    senha: "",
    ativo: true,
};

export default function UserModal({
    isOpen,
    onClose,
    onSave,
    user,
    loading = false,
}) {
    const [form, setForm] = useState(INITIAL_FORM);

    useEffect(() => {
        if (!isOpen) {
            return;
        }

        if (user) {
            setForm({
                nome: user.nome ?? "",
                email: user.email ?? "",
                telefone: user.telefone ?? "",
                matricula: user.matricula ?? "",
                senha: "",
                ativo: user.ativo ?? true,
            });

            return;
        }

        setForm(INITIAL_FORM);
    }, [isOpen, user]);

    function handleChange(event) {
        const { name, value, type, checked } = event.target;

        setForm((previous) => ({
            ...previous,
            [name]: type === "checkbox" ? checked : value,
        }));
    }

    function handleSubmit(event) {
        event.preventDefault();

        const payload = user
            ? {
                  nome: form.nome,
                  email: form.email,
                  telefone: form.telefone || null,
                  matricula: form.matricula || null,
                  ativo: form.ativo,
              }
            : {
                  nome: form.nome,
                  email: form.email,
                  telefone: form.telefone || null,
                  matricula: form.matricula || null,
                  senha: form.senha,
              };

        onSave(payload);
    }

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title={user ? "Editar Usuário" : "Novo Usuário"}
            width="650px"
        >
            <form onSubmit={handleSubmit}>

                <div className="form-group">
                    <label htmlFor="nome">Nome</label>

                    <input
                        id="nome"
                        name="nome"
                        type="text"
                        value={form.nome}
                        onChange={handleChange}
                        required
                        minLength={3}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="email">E-mail</label>

                    <input
                        id="email"
                        name="email"
                        type="email"
                        value={form.email}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="telefone">Telefone</label>

                    <input
                        id="telefone"
                        name="telefone"
                        type="text"
                        value={form.telefone}
                        onChange={handleChange}
                        placeholder="11999998888"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="matricula">Matrícula</label>

                    <input
                        id="matricula"
                        name="matricula"
                        type="text"
                        value={form.matricula}
                        onChange={handleChange}
                    />
                </div>

                {!user && (
                    <div className="form-group">
                        <label htmlFor="senha">
                            Senha
                        </label>

                        <input
                            id="senha"
                            name="senha"
                            type="password"
                            value={form.senha}
                            onChange={handleChange}
                            required
                            minLength={6}
                        />
                    </div>
                )}

                {user && (
                    <div className="form-group">
                        <label>
                            <input
                                type="checkbox"
                                name="ativo"
                                checked={form.ativo}
                                onChange={handleChange}
                            />

                            {" "}
                            Usuário ativo
                        </label>
                    </div>
                )}

                <div className="modal-actions">

                    <button
                        type="button"
                        onClick={onClose}
                        disabled={loading}
                    >
                        Cancelar
                    </button>

                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading
                            ? "Salvando..."
                            : user
                                ? "Atualizar"
                                : "Cadastrar"}
                    </button>

                </div>

            </form>
        </Modal>
    );
}

UserModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onSave: PropTypes.func.isRequired,
    user: PropTypes.object,
    loading: PropTypes.bool,
};

UserModal.defaultProps = {
    user: null,
    loading: false,
};