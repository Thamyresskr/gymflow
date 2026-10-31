
/**
 * Página inicial da aplicação.
 *
 * ADMIN, RECEPCAO e PROFESSOR: indicadores completos.
 * ALUNO: somente ocupação atual.
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

const FUSO_HORARIO = "America/Sao_Paulo";

/**
 * Formata o horário de um registro para o horário de Brasília.
 *
 * Valores sem indicação de fuso são interpretados como UTC,
 * conforme a convenção de armazenamento esperada pelo backend.
 */
function formatarHorarioBrasilia(valor) {
    if (!valor) {
        return "—";
    }

    const dataComFuso =
        typeof valor === "string" &&
        !/(Z|[+-]\d{2}:\d{2})$/i.test(valor)
            ? `${valor}Z`
            : valor;

    const data = new Date(dataComFuso);

    if (Number.isNaN(data.getTime())) {
        return "—";
    }

    return new Intl.DateTimeFormat("pt-BR", {
        timeZone: FUSO_HORARIO,
        hour: "2-digit",
        minute: "2-digit",
    }).format(data);
}

function Dashboard() {
    const { user } = useAuthContext();

    const tipoUsuario = String(
        user?.tipo ?? user?.role ?? "",
    ).toUpperCase();

    const acessoAdministrativo = [
        USER_ROLES.ADMIN,
        USER_ROLES.RECEPCAO,
        USER_ROLES.PROFESSOR,
    ].includes(tipoUsuario);

    const [dashboard, setDashboard] = useState(null);
    const [ocupacao, setOcupacao] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [reloadKey, setReloadKey] = useState(0);

    /**
     * Carrega os indicadores conforme o perfil do usuário.
     */
    const carregarDashboard = useCallback(async () => {
        if (acessoAdministrativo) {
            return getDashboard();
        }

        return getOcupacao();
    }, [acessoAdministrativo]);

    /**
     * Carregamento inicial e atualização quando o perfil
     * ou a solicitação de recarga mudar.
     */
    useEffect(() => {
        let active = true;

        async function buscarDados() {
            try {
                const dados = await carregarDashboard();

                if (!active) {
                    return;
                }

                if (acessoAdministrativo) {
                    setDashboard(dados);
                    setOcupacao(null);
                } else {
                    setOcupacao(dados);
                    setDashboard(null);
                }

                setError(null);
            } catch (err) {
                console.error(
                    "Erro ao carregar Dashboard:",
                    err,
                );

                if (active) {
                    setError(err);
                }
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        }

        void buscarDados();

        return () => {
            active = false;
        };
    }, [
        carregarDashboard,
        acessoAdministrativo,
        reloadKey,
    ]);

    /**
     * Solicita uma nova consulta dos indicadores.
     */
    const handleTentarNovamente = () => {
        setLoading(true);
        setError(null);
        setReloadKey((valorAtual) => valorAtual + 1);
    };

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
                    onClick={handleTentarNovamente}
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
                            <span>Horário (Brasília)</span>
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
                                        {formatarHorarioBrasilia(
                                            item.entrada,
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
