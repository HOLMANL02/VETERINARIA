import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/useAuth";

export default function LoginPage() {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(false);

  const { iniciarSesion } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const destino = location.state?.from ?? "/";

  async function manejarSubmit(e) {
    e.preventDefault();
    setError("");
    setCargando(true);
    try {
      await iniciarSesion(correo, password);
      navigate(destino, { replace: true });
    } catch (err) {
  if (err.response?.status === 401) {
    setError("Correo o contraseña incorrectos");
  } else if (err.response?.status === 403) {
    setError("Este usuario está desactivado");
  } else if (err.response?.status === 404) {
    setError("El servidor no reconoce /auth/me. Verifica que el backend tenga ese endpoint y se haya reiniciado.");
  } else if (err.response) {
    setError(`El servidor respondió con un error (${err.response.status}). Revisa los logs del backend.`);
  } else {
    setError("No se pudo conectar con el servidor. Intenta de nuevo.");
  }
} finally {
      setCargando(false);
    }
  }

  return (
    <div className="login-screen">
      <aside className="login-brand">
        <div className="login-brand-mark" aria-hidden="true">
          <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="18" r="6" fill="currentColor" opacity="0.9" />
            <circle cx="36" cy="14" r="6" fill="currentColor" opacity="0.9" />
            <circle cx="48" cy="26" r="6" fill="currentColor" opacity="0.9" />
            <path
              d="M14 42c0-9 8-14 18-14s18 5 18 14c0 7-6 10-13 10-3 0-4-2-5-2s-2 2-5 2c-7 0-13-3-13-10Z"
              fill="currentColor"
            />
          </svg>
        </div>
        <h1>Veterinaria</h1>
        <p>
          Historias clínicas, citas e inventario en un solo lugar para tu
          equipo.
        </p>
      </aside>

      <main className="login-form-panel">
        <form className="login-card" onSubmit={manejarSubmit}>
          <h2>Iniciar sesión</h2>
          <p className="subtitle">Ingresa con tu cuenta del sistema</p>

          {error && <div className="error-box">{error}</div>}

          <div className="field">
            <label htmlFor="correo">Correo</label>
            <input
              id="correo"
              type="email"
              placeholder="nombre@veterinaria.com"
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              required
              autoFocus
            />
          </div>

          <div className="field">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            className="btn-primary"
            type="submit"
            disabled={cargando}
            style={{ width: "100%" }}
          >
            {cargando ? "Ingresando..." : "Ingresar"}
          </button>
        </form>
      </main>
    </div>
  );
}
