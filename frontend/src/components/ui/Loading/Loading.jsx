/**
 * Componente reutilizável de carregamento.
 *
 * Pode ser utilizado em qualquer página da aplicação.
 */

import PropTypes from "prop-types";
import "./Loading.css";

function Loading({
    text = "Carregando...",
    fullScreen = false,
}) {
    return (
        <div
            className={`loading-container ${
                fullScreen ? "loading-fullscreen" : ""
            }`}
            role="status"
            aria-live="polite"
        >
            <div className="loading-spinner" aria-hidden="true" />

            <p className="loading-text">
                {text}
            </p>
        </div>
    );
}

Loading.propTypes = {
    text: PropTypes.string,
    fullScreen: PropTypes.bool,
};

export default Loading;