/**
 * Página inicial da aplicação.
 *
 * ADMIN e RECEPCAO: indicadores administrativos.
 * ALUNO e PROFESSOR: somente ocupação atual.
 */

import { useCallback, useEffect, useState } from "react";

import EmptyState from "@/components/ui/EmptyState/EmptyState";
import Loading from "@/components/ui/Loading/Loading";
import { useAuthContext } from "@/contexts/AuthContext";
import { USER_ROLES } from "@/constants/roles";
import {
    getDashboard,
    getOcupacao,
} from "@/services/dashboardService";

import DashboardCards from "./components/DashboardCards";
import styles from "./Dashboard.module.css";

function Dashboard() {
    const { user } = useAuthContext();

    const tipoUsuario = String(
        user?.tipo ?? user?.role ?? "",
    ).toUpperCase();

    const acessoAdministrativo = [
        USER_ROLES.ADMIN,
        USER_ROLES.RECEPCAO,
    ].includes(tipoUsuario);

    const [dashboard, setDashboard] = useState(null);
    const [ocupacao, setOcupacao] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const carregarDashboard = useCallback(
        async (isActive = () => true) => {
            try {
                setError(null);

                if (acessoAdministrativo) {
                    const dados = await getDashboard();

                    if (isActive()) {
                        setDashboard(dados);
                    }
                } else {
                    const dados = await getOcupacao();

                    if (isActive()) {
                        setOcupacao(dados);
                    }
                }
            } catch (err) {
                console.error(
                    "Erro ao carregar Dashboard:",
                    err,
                );

                if (isActive()) {
                    setError(err);
                }
            } finally {
                if (isActive()) {
                    setLoading(false);
                }
            }
        },
        [acessoAdministrativo],
    );

    useEffect(() => {
        let active = true;

        void carregarDashboard(() => active);

        return () => {
            active = false;
        };
    }, [carregarDashboard]);

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

                <button
                    type="button"
                    onClick={() => {
                        setLoading(true);
                        void carregarDashboard();
                    }}
                >
                    Tentar novamente
                </button>
            </section>
        );
    }

    const resumo = dashboard?.resumo ?? {};
    const ultimosCheckins =
        dashboard?.ultimos_checkins ?? [];

    const dashboardData = acessoAdministrativo
        ? [
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
                value: `${Number(
                    resumo.tempo_medio_permanencia ?? 0,
                ).toFixed(2)} min`,
            },
        ]
        : [
            {
                title: "Pessoas na Academia",
                value: ocupacao?.ocupacao_atual ?? 0,
            },
        ];

    return (
        <section className={styles.container}>
            <header className={styles.header}>
                <h1>Dashboard</h1>

                <p>
                    Olá,{" "}
                    <strong>
                        {user?.nome ?? user?.name ?? "Usuário"}
                    </strong>
                    ! Bem-vindo ao{" "}
                    <strong>GymFlow</strong>.
                </p>
            </header>

            <DashboardCards data={dashboardData} />

            {acessoAdministrativo && (
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
            )}
        </section>
    );
}

export default Dashboard;
