import PropTypes from "prop-types";
import Modal from "../Modal/Modal";
import styles from "./ConfirmDialog.module.css";

export default function ConfirmDialog({
    isOpen,
    title = "Confirmação",
    message,
    confirmText = "Confirmar",
    cancelText = "Cancelar",
    loading = false,
    onConfirm,
    onCancel,
}) {
    return (
        <Modal isOpen={isOpen} onClose={onCancel} width="420px">
            <div className={styles.container}>
                <h2 className={styles.title}>{title}</h2>

                <p className={styles.message}>{message}</p>

                <div className={styles.actions}>
                    <button
                        type="button"
                        className={styles.cancelButton}
                        onClick={onCancel}
                        disabled={loading}
                    >
                        {cancelText}
                    </button>

                    <button
                        type="button"
                        className={styles.confirmButton}
                        onClick={onConfirm}
                        disabled={loading}
                    >
                        {loading ? "Aguarde..." : confirmText}
                    </button>
                </div>
            </div>
        </Modal>
    );
}

ConfirmDialog.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    title: PropTypes.string,
    message: PropTypes.string.isRequired,
    confirmText: PropTypes.string,
    cancelText: PropTypes.string,
    loading: PropTypes.bool,
    onConfirm: PropTypes.func.isRequired,
    onCancel: PropTypes.func.isRequired,
};