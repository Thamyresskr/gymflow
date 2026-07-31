/**
 * Lista de indicadores do Dashboard.
 *
 * Responsabilidades:
 * - Renderizar os indicadores do Dashboard.
 * - Delegar a exibição de cada indicador ao DashboardCard.
 */

import PropTypes from "prop-types";

import DashboardCard from "./DashboardCard";

import styles from "../Dashboard.module.css";

/**
 * Lista de cards do Dashboard.
 *
 * @param {Object} props
 * @param {Array} props.data
 */
function DashboardCards({ data }) {
    return (
        <section
            className={styles.cards}
            aria-label="Indicadores do Dashboard"
        >
            {data.map((item) => (
                <DashboardCard
                    key={item.title}
                    title={item.title}
                    value={item.value}
                />
            ))}
        </section>
    );
}

DashboardCards.propTypes = {
    data: PropTypes.arrayOf(
        PropTypes.shape({
            title: PropTypes.string.isRequired,
            value: PropTypes.oneOfType([
                PropTypes.string,
                PropTypes.number,
            ]).isRequired,
        }),
    ).isRequired,
};

export default DashboardCards;