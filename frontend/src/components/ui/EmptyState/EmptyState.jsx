/**
 * Componente reutilizável para estados sem conteúdo.
 */

import PropTypes from "prop-types";
import "./EmptyState.css";

function EmptyState({
    title = "Nenhum registro encontrado",
    description = "Não há informações para exibir no momento.",
}) {
    return (
        <div
            className="empty-state"
            role="status"
            aria-live="polite"
        >
            <div
                className="empty-state-icon"
                aria-hidden="true"
            >
                📭
            </div>

            <h2 className="empty-state-title">
                {title}
            </h2>

            <p className="empty-state-description">
                {description}
            </p>
        </div>
    );
}

EmptyState.propTypes = {
    title: PropTypes.string,
    description: PropTypes.string,
};

export default EmptyState;