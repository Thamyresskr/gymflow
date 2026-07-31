/**
 * Card de um registro de check-in.
 */

import StatusBadge from "./StatusBadge";

import styles from "../Checkins.module.css";

function CheckinCard({
    item,
    onCheckout,
    submitting,
}) {
    const ativo = !item.checkout_time;

    return (
        <article className={styles.card}>
            <div className={styles.info}>
                <h3 className={styles.title}>
                    Usuário #{item.user_id}
                </h3>

                <span className={styles.subtitle}>
                    Entrada:{" "}
                    {new Date(
                        item.checkin_time,
                    ).toLocaleString("pt-BR")}
                </span>

                {item.checkout_time && (
                    <span className={styles.subtitle}>
                        Saída:{" "}
                        {new Date(
                            item.checkout_time,
                        ).toLocaleString("pt-BR")}
                    </span>
                )}
            </div>

            <div className={styles.right}>
                <StatusBadge active={ativo} />

                {ativo && (
                    <button
                        type="button"
                        className={styles.secondaryButton}
                        disabled={submitting}
                        onClick={() => onCheckout(item.id)}
                    >
                        {submitting
                            ? "Finalizando..."
                            : "Registrar Check-out"}
                    </button>
                )}
            </div>
        </article>
    );
}

export default CheckinCard;