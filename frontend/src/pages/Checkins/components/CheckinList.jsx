/**
 * Lista de check-ins.
 */

import CheckinCard from "./CheckinCard";

import styles from "../Checkins.module.css";

function CheckinList({
    checkins,
    onCheckout,
    submitting,
}) {
    return (
        <section className={styles.list}>
            {checkins.map((item) => (
                <CheckinCard
                    key={item.id}
                    item={item}
                    onCheckout={onCheckout}
                    submitting={submitting}
                />
            ))}
        </section>
    );
}

export default CheckinList;