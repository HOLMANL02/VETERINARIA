import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/useAuth";

const ENLACES = [
  { to: "/", label: "Inicio", roles: null },
  { to: "/clientes", label: "Clientes", roles: ["administrador", "recepcionista"] },
  { to: "/usuarios", label: "Usuarios", roles: ["administrador"] },
];

export default function Layout() {
  const { usuario, cerrarSesion } = useAuth();

  const enlacesVisibles = ENLACES.filter(
    (enlace) => !enlace.roles || enlace.roles.includes(usuario.rol)
  );

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">Veterinaria</div>

        <nav className="sidebar-nav">
          {enlacesVisibles.map((enlace) => (
            <NavLink
              key={enlace.to}
              to={enlace.to}
              end={enlace.to === "/"}
              className={({ isActive }) =>
                isActive ? "sidebar-link active" : "sidebar-link"
              }
            >
              {enlace.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user">
            {usuario.nombre}
            <span className="rol">{usuario.rol}</span>
          </div>
          <button className="btn-secondary" onClick={cerrarSesion} style={{ width: "100%" }}>
            Cerrar sesión
          </button>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
