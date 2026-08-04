/**
 * Página inicial da aplicação.
 *
 * Responsabilidades:
 * - Buscar os indicadores do Dashboard.
 * - Exibir os principais indicadores da academia.
 * - Exibir os últimos check-ins registrados.
 */

import { useEffect, useState } from "react";

import EmptyState from "@/components/ui/EmptyState/EmptyState";
import Loading from "@/components/ui/Loading/Loading";
import { useAuthContext } from "@/contexts/AuthContext";
import { getDashboard } from "@/services/dashboardService";

import DashboardCards from "./components/DashboardCards";

import styles from "./Dashboard.module.css";

function Dashboard() {
    const { user } = useAuthContext();

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    /**
     * Carrega os indicadores do Dashboard.
     */
    async function carregarDashboard() {
        try {
            setLoading(true);
            setError(null);

            const dados = await getDashboard();

            setDashboard(dados);
        } catch (err) {
            console.error("Erro ao carregar Dashboard:", err);
            setError(err);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        carregarDashboard();
    }, []);

    if (loading) {
        return (
            <Loading
                fullScreen
                text="Carregando dashboard..."
            />
        );
    }

    if (error) {
        return (
            <section className={styles.container}>
                <h2>Erro ao carregar os indicadores.</h2>

                <p>
                    Não foi possível consultar os dados da API.
                </p>
            </section>
        );
    }

    const resumo = dashboard?.resumo ?? {};

    const ultimosCheckins =
        dashboard?.ultimos_checkins ?? [];

    const dashboardData = [
        {
            title: "Ocupação Atual",
            value: resumo.ocupacao_atual ?? 0,
        },
        {
            title: "Check-ins Hoje",
            value: resumo.checkins_hoje ?? 0,
        },
        {
            title: "Check-outs Hoje",
            value: resumo.checkouts_hoje ?? 0,
        },
        {
            title: "Tempo Médio",
            value: `${(
                resumo.tempo_medio_permanencia ?? 0
            ).toFixed(2)} min`,
        },
    ];

    return (
        <section className={styles.container}>
            <header className={styles.header}>
                <h1>Dashboard</h1>

                <p>
                    Olá,{" "}
                    <strong>
                        {user?.name ?? "Usuário"}
                    </strong>
                    ! Bem-vindo ao{" "}
                    <strong>GymFlow</strong>.
                </p>
            </header>

            <DashboardCards data={dashboardData} />

            <section className={styles.panel}>
                <h2>Últimos Check-ins</h2>

                <div className={styles.table}>
                    <div className={styles.tableHeader}>
                        <span>Usuário</span>
                        <span>Status</span>
                        <span>Horário</span>
                    </div>

                    {ultimosCheckins.length === 0 ? (
                        <EmptyState
                            title="Nenhum check-in encontrado"
                            description="Os registros aparecerão aqui quando houver movimentação."
                        />
                    ) : (
                        ultimosCheckins.map((item) => (
                            <div
                                key={`${item.usuario}-${item.entrada}`}
                                className={styles.row}
                            >
                                <span>{item.usuario}</span>

                                <span>
                                    {item.saida
                                        ? "Saída"
                                        : "Entrada"}
                                </span>

                                <span>
                                    {new Date(
                                        item.entrada,
                                    ).toLocaleTimeString(
                                        "pt-BR",
                                        {
                                            hour: "2-digit",
                                            minute: "2-digit",
                                        },
                                    )}
                                </span>
                            </div>
                        ))
                    )}
                </div>
            </section>
        </section>
    );
}

export default Dashboard;