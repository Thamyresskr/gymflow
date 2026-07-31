/**
 * Serviço centralizado de notificações da aplicação.
 *
 * Responsabilidades:
 * - Exibir mensagens de sucesso.
 * - Exibir mensagens de erro.
 * - Exibir mensagens informativas.
 * - Exibir mensagens de aviso.
 */

import toast from "react-hot-toast";

/**
 * Exibe uma notificação de sucesso.
 *
 * @param {string} message
 */
export function notifySuccess(message) {
    toast.success(message);
}

/**
 * Exibe uma notificação de erro.
 *
 * @param {string} message
 */
export function notifyError(message) {
    toast.error(message);
}

/**
 * Exibe uma notificação informativa.
 *
 * @param {string} message
 */
export function notifyInfo(message) {
    toast(message);
}

/**
 * Exibe uma notificação de aviso.
 *
 * @param {string} message
 */
export function notifyWarning(message) {
    toast(message, {
        icon: "⚠️",
    });
}