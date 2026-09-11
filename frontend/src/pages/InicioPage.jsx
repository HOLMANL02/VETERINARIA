import { useAuth } from "../context/useAuth";

export default function InicioPage() {
  const { usuario } = useAuth();

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Bienvenido</h1>
          <p>Sesión iniciada como {usuario.rol}.</p>
        </div>
      </div>
      <div className="card" style={{ padding: 24 }}>
        <p style={{ margin: 0, color: "var(--color-text-muted)" }}>
          Usa el menú de la izquierda para gestionar clientes
          {usuario.rol === "administrador" ? " y usuarios" : ""}.
        </p>
      </div>
    </div>
  );
}
