
/**
 * Página de gerenciamento de check-ins.
 *
 * Responsabilidades:
 * - Buscar o histórico de check-ins conforme o perfil.
 * - Registrar novos check-ins.
 * - Registrar check-out.
 * - Atualizar a lista após operações.
 */

import { useCallback, useEffect, useState } from "react";

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

    const role = String(user?.role ?? "").toUpperCase();

    const podeConsultarHistoricoCompleto = [
        USER_ROLES.ADMIN,
        USER_ROLES.RECEPCAO,
    ].includes(role);

    /**
     * Carrega os check-ins conforme as permissões do perfil.
     * ADMIN e RECEPCAO consultam o histórico completo.
     * PROFESSOR e ALUNO consultam apenas o próprio histórico.
     */
    const carregarCheckins = useCallback(async () => {
        if (!user) {
            setCheckins([]);
            setLoading(false);
            setError(null);
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const dados = podeConsultarHistoricoCompleto
                ? await getCheckins()
                : await getMyCheckins();

            setCheckins(Array.isArray(dados) ? dados : []);
        } catch (err) {
            console.error("Erro ao carregar check-ins:", err);
            setError(err);
        } finally {
            setLoading(false);
        }
    }, [user, podeConsultarHistoricoCompleto]);

    useEffect(() => {
        void carregarCheckins();
    }, [carregarCheckins]);

    /**
     * Registra um novo check-in.
     */
    const handleNovoCheckin = useCallback(async () => {
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
    }, [carregarCheckins]);

    /**
     * Registra o check-out.
     */
    const handleCheckout = useCallback(
        async (checkinId) => {
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
        },
        [carregarCheckins],
    );

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

                <button
                    type="button"
                    className={styles.primaryButton}
                    onClick={carregarCheckins}
                >
                    Tentar novamente
                </button>
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
                    disabled={submitting || !user}
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
