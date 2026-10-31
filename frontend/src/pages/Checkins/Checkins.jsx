
/**
 * Página de gerenciamento de check-ins.
 *
 * Responsabilidades:
 * - Buscar o histórico conforme o perfil.
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
    const [reloadKey, setReloadKey] = useState(0);

    const role = String(user?.role ?? "").toUpperCase();

    const podeConsultarHistoricoCompleto = [
        USER_ROLES.ADMIN,
        USER_ROLES.RECEPCAO,
    ].includes(role);

    /**
     * Busca os check-ins conforme as permissões do perfil.
     */
    const buscarCheckins = useCallback(async () => {
        if (!user) {
            return [];
        }

        const dados = podeConsultarHistoricoCompleto
            ? await getCheckins()
            : await getMyCheckins();

        return Array.isArray(dados) ? dados : [];
    }, [user, podeConsultarHistoricoCompleto]);

    /**
     * Atualiza a lista de check-ins.
     */
    const atualizarCheckins = useCallback(async () => {
        const dados = await buscarCheckins();

        setCheckins(dados);
        setError(null);
    }, [buscarCheckins]);

    /**
     * Carregamento inicial e atualização da lista.
     */
    useEffect(() => {
        let active = true;

        async function carregarDados() {
            try {
                const dados = await buscarCheckins();

                if (active) {
                    setCheckins(dados);
                    setError(null);
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

        void carregarDados();

        return () => {
            active = false;
        };
    }, [buscarCheckins, reloadKey]);

    /**
     * Solicita uma nova consulta dos check-ins.
     */
    const handleTentarNovamente = () => {
        setLoading(true);
        setError(null);
        setReloadKey((valorAtual) => valorAtual + 1);
    };

    /**
     * Registra um novo check-in.
     */
    const handleNovoCheckin = useCallback(async () => {
        try {
            setSubmitting(true);

            await registerCheckin();
            await atualizarCheckins();
        } catch (err) {
            console.error("Erro ao registrar check-in:", err);

            alert(
                err.response?.data?.detail ??
                    "Não foi possível registrar o check-in.",
            );
        } finally {
            setSubmitting(false);
        }
    }, [atualizarCheckins]);

    /**
     * Registra o check-out.
     */
    const handleCheckout = useCallback(
        async (checkinId) => {
            try {
                setSubmitting(true);

                await registerCheckout(checkinId);
                await atualizarCheckins();
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
        [atualizarCheckins],
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
                    onClick={handleTentarNovamente}
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
