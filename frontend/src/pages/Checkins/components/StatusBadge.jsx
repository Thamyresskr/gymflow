/**
 * Badge de status do check-in.
 */

import styles from "../Checkins.module.css";

function StatusBadge({ active }) {
    return (
        <span
            className={`${styles.badge} ${
                active
                    ? styles.active
                    : styles.finished
            }`}
        >
            {active ? "Ativo" : "Finalizado"}
        </span>
    );
}

export default StatusBadge;