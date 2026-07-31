/**
 * Página de autenticação da aplicação.
 *
 * Responsabilidades:
 * - Autenticar o usuário.
 * - Exibir mensagens de erro.
 * - Redirecionar para a área protegida.
 */

import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "@/hooks/useAuth";

import styles from "./Login.module.css";


function Login() {
    const navigate = useNavigate();
    const location = useLocation();

    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    /**
     * Página que o usuário tentou acessar
     * antes de ser redirecionado para o login.
     */
    const redirectTo =
        location.state?.from?.pathname || "/dashboard";


    /**
     * Realiza a autenticação.
     */
    async function handleSubmit(event) {
        event.preventDefault();

        if (loading) {
            return;
        }

        setError("");
        setLoading(true);

        try {
            await login(
                email.trim(),
                password,
            );

            navigate(redirectTo, {
                replace: true,
            });

        } catch (err) {

            const message =
                err.response?.data?.message ??
                err.response?.data?.detail ??
                "E-mail ou senha inválidos.";

            setError(message);

        } finally {
            setLoading(false);
        }
    }


    return (
        <div className={styles.container}>

            <div className={styles.card}>

                <h1>
                    GymFlow
                </h1>


                <p>
                    Controle Inteligente de Ocupação
                </p>


                <form onSubmit={handleSubmit}>


                    <input
                        type="email"
                        placeholder="E-mail"
                        autoComplete="username"
                        autoFocus
                        value={email}
                        onChange={(event) =>
                            setEmail(event.target.value)
                        }
                        required
                    />


                    <input
                        type="password"
                        placeholder="Senha"
                        autoComplete="current-password"
                        value={password}
                        onChange={(event) =>
                            setPassword(event.target.value)
                        }
                        required
                    />


                    {error && (

                        <span
                            className={styles.error}
                            aria-live="polite"
                        >
                            {error}
                        </span>

                    )}


                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {
                            loading
                                ? "Entrando..."
                                : "Entrar"
                        }

                    </button>


                </form>

            </div>

        </div>
    );
}


export default Login;