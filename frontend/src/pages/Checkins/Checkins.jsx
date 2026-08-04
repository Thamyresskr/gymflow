/**
 * Página de gerenciamento de check-ins.
 *
 * Responsabilidades:
 * - Buscar o histórico de check-ins.
 * - Registrar novos check-ins.
 * - Registrar check-out.
 * - Atualizar a lista automaticamente.
 */

import { useEffect, useState } from "react";


import EmptyState from "@/components/ui/EmptyState/EmptyState";
import Loading from "@/components/ui/Loading/Loading";
import { USER_ROLES } from "@/constants/roles";
import { useAuthContext } from "@/contexts/AuthContext";

import {
    getCheckins,
    getMyCheckins,
    registerCheckin,
    registerCheckout,
} from "@/services/checkinService";

import CheckinList from "./components/CheckinList";

import styles from "./Checkins.module.css";

function Checkins() {
    const { user } = useAuthContext();

    const [checkins, setCheckins] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [submitting, setSubmitting] = useState(false);

    /**
     * Carrega o histórico de check-ins.
     */
    async function carregarCheckins() {
        try {
            setLoading(true);
            setError(null);

            const dados =
                user?.role === USER_ROLES.ALUNO
                    ? await getMyCheckins()
                    : await getCheckins();

            setCheckins(dados);
        } catch (err) {
            console.error("Erro ao carregar check-ins:", err);
            setError(err);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        if (user) {
            carregarCheckins();
        }
    }, [user]);

    /**
     * Registra um novo check-in.
     */
    async function handleNovoCheckin() {
        try {
            setSubmitting(true);

            await registerCheckin();
            await carregarCheckins();
        } catch (err) {
            console.error("Erro ao registrar check-in:", err);

            alert(
                err.response?.data?.detail ??
                    "Não foi possível registrar o check-in.",
            );
        } finally {
            setSubmitting(false);
        }
    }

    /**
     * Registra o check-out.
     */
    async function handleCheckout(checkinId) {
        try {
            setSubmitting(true);

            await registerCheckout(checkinId);
            await carregarCheckins();
        } catch (err) {
            console.error("Erro ao registrar check-out:", err);

            alert(
                err.response?.data?.detail ??
                    "Não foi possível registrar o check-out.",
            );
        } finally {
            setSubmitting(false);
        }
    }

    if (loading) {
        return (
            <Loading
                fullScreen
                text="Carregando check-ins..."
            />
        );
    }

    if (error) {
        return (
            <section className={styles.container}>
                <h2>Erro ao carregar os check-ins.</h2>

                <p>
                    Não foi possível consultar os dados da API.
                </p>
            </section>
        );
    }

    return (
        <section className={styles.container}>
            <header className={styles.header}>
                <h1>Check-ins</h1>

                <p>
                    Histórico de entradas e saídas da academia.
                </p>
            </header>

            <div className={styles.actions}>
                <button
                    type="button"
                    className={styles.primaryButton}
                    disabled={submitting}
                    onClick={handleNovoCheckin}
                >
                    {submitting
                        ? "Processando..."
                        : "Novo Check-in"}
                </button>
            </div>

            {checkins.length === 0 ? (
                <EmptyState
                    title="Nenhum check-in encontrado"
                    description="Os registros aparecerão aqui quando houver movimentação."
                />
            ) : (
                <CheckinList
                    checkins={checkins}
                    onCheckout={handleCheckout}
                    submitting={submitting}
                />
            )}
        </section>
    );
}

export default Checkins;