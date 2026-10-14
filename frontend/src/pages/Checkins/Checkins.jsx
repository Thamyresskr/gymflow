
/**
 * Página de gerenciamento de check-ins.
 *
 * Responsabilidades:
 * - Buscar o histórico de check-ins.
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

    /**
     * Carrega o histórico de check-ins do usuário.
     */
    const carregarCheckins = useCallback(async () => {
        if (!user) {
            setCheckins([]);
            setLoading(false);
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const dados =
                user.role === USER_ROLES.ALUNO
                    ? await getMyCheckins()
                    : await getCheckins();

            setCheckins(Array.isArray(dados) ? dados : []);
        } catch (err) {
            console.error("Erro ao carregar check-ins:", err);
            setError(err);
        } finally {
            setLoading(false);
        }
    }, [user]);

    /**
     * Busca os registros quando o usuário estiver disponível.
     */
    useEffect(() => {
        if (!user) {
            return;
        }

        let active = true;

        async function carregar() {
            setLoading(true);
            setError(null);

            try {
                const dados =
                    user.role === USER_ROLES.ALUNO
                        ? await getMyCheckins()
                        : await getCheckins();

                if (active) {
                    setCheckins(Array.isArray(dados) ? dados : []);
                }
            } catch (err) {
                console.error("Erro ao carregar check-ins:", err);

                if (active) {
                    setError(err);
                }
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        }

        void carregar();

        return () => {
            active = false;
        };
    }, [user]);

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
    const handleCheckout = useCallback(async (checkinId) => {
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
    }, [carregarCheckins]);

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
