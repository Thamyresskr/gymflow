/**
 * Card de indicador do Dashboard.
 *
 * Responsabilidades:
 * - Exibir um indicador.
 * - Exibir o ícone correspondente.
 */

import PropTypes from "prop-types";

import {
    Clock,
    HelpCircle,
    LogIn,
    LogOut,
    Users,
} from "lucide-react";

import styles from "../Dashboard.module.css";

/**
 * Ícones disponíveis para os indicadores.
 */
const ICONS = Object.freeze({
    "Ocupação Atual": <Users size={26} />,
    "Check-ins Hoje": <LogIn size={26} />,
    "Check-outs Hoje": <LogOut size={26} />,
    "Tempo Médio": <Clock size={26} />,
});

/**
 * Card de indicador.
 *
 * @param {Object} props
 * @param {string} props.title
 * @param {string|number} props.value
 */
function DashboardCard({ title, value }) {
    const icon = ICONS[title] ?? (
        <HelpCircle size={26} />
    );

    return (
        <article className={styles.card}>
            <div className={styles.cardTop}>
                <span
                    className={styles.icon}
                    aria-hidden="true"
                >
                    {icon}
                </span>

                <span className={styles.cardTitle}>
                    {title}
                </span>
            </div>

            <strong className={styles.cardValue}>
                {value}
            </strong>
        </article>
    );
}

DashboardCard.propTypes = {
    title: PropTypes.string.isRequired,
    value: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number,
    ]).isRequired,
};

export default DashboardCard;