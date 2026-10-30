
/**
 * Cadastro de alunos realizado pela RECEPÇÃO.
 *
 * Responsabilidades:
 * - Cadastrar exclusivamente alunos.
 * - Validar os campos obrigatórios.
 * - Integrar com o serviço de cadastro da recepção.
 * - Informar o resultado da operação.
 *
 * O perfil ALUNO é definido pelo backend.
 */

import { useState } from "react";

import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

import { createReceptionStudent } from "@/services/userService";
import {
    notifySuccess,
    notifyError,
} from "@/services/notificationService";

import styles from "./StudentRegistration.module.css";

const INITIAL_FORM = {
    nome: "",
    email: "",
    telefone: "",
    matricula: "",
    senha: "",
};

function StudentRegistration() {
    const [form, setForm] = useState(INITIAL_FORM);
    const [loading, setLoading] = useState(false);

    function handleChange(event) {
        const { name, value } = event.target;

        setForm((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    function validateForm() {
        if (form.nome.trim().length < 3) {
            notifyError("Informe um nome com pelo menos 3 caracteres.");
            return false;
        }

        if (!form.email.trim()) {
            notifyError("Informe o e-mail do aluno.");
            return false;
        }

        if (form.senha.length < 6) {
            notifyError("A senha deve possuir pelo menos 6 caracteres.");
            return false;
        }

        const telefone = form.telefone.replace(/\D/g, "");

        if (telefone && ![10, 11].includes(telefone.length)) {
            notifyError("Informe um telefone válido com DDD.");
            return false;
        }

        return true;
    }

    async function handleSubmit(event) {
        event.preventDefault();

        if (!validateForm()) {
            return;
        }

        const payload = {
            nome: form.nome.trim(),
            email: form.email.trim(),
            telefone: form.telefone.replace(/\D/g, "") || null,
            matricula: form.matricula.trim() || null,
            senha: form.senha,
        };

        try {
            setLoading(true);

            await createReceptionStudent(payload);

            notifySuccess("Aluno cadastrado com sucesso!");

            setForm(INITIAL_FORM);
        } catch (error) {
            const message =
                error.response?.data?.detail ||
                "Não foi possível cadastrar o aluno.";

            notifyError(
                typeof message === "string"
                    ? message
                    : "Verifique os dados informados.",
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className={styles.container}>
            <header className={styles.header}>
                <div>
                    <h1>Cadastro de Alunos</h1>
                    <p>
                        Cadastre novos alunos no sistema GymFlow.
                    </p>
                </div>
            </header>

            <section className={styles.card}>
                <div className={styles.sectionHeader}>
                    <h2>Dados do aluno</h2>
                    <p>
                        Preencha as informações para realizar o cadastro.
                    </p>
                </div>

                <form
                    className={styles.form}
                    onSubmit={handleSubmit}
                >
                    <Input
                        id="nome"
                        name="nome"
                        label="Nome completo"
                        value={form.nome}
                        onChange={handleChange}
                        required
                        minLength={3}
                        maxLength={100}
                        autoComplete="name"
                        autoFocus
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
                        placeholder="11999998888"
                        maxLength={15}
                        autoComplete="tel"
                    />

                    <Input
                        id="matricula"
                        name="matricula"
                        label="Matrícula"
                        value={form.matricula}
                        onChange={handleChange}
                        maxLength={20}
                    />

                    <Input
                        id="senha"
                        name="senha"
                        label="Senha inicial"
                        type="password"
                        value={form.senha}
                        onChange={handleChange}
                        required
                        minLength={6}
                        maxLength={100}
                        autoComplete="new-password"
                        placeholder="Mínimo de 6 caracteres"
                    />

                    <div className={styles.info}>
                        O aluno será cadastrado automaticamente com o
                        perfil ALUNO.
                    </div>

                    <div className={styles.actions}>
                        <Button
                            type="button"
                            variant="secondary"
                            disabled={loading}
                            onClick={() => setForm(INITIAL_FORM)}
                        >
                            Limpar
                        </Button>

                        <Button
                            type="submit"
                            variant="primary"
                            loading={loading}
                            disabled={loading}
                        >
                            Cadastrar aluno
                        </Button>
                    </div>
                </form>
            </section>
        </main>
    );
}

export default StudentRegistration;
