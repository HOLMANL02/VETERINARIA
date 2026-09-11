import { Navigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";

export default function ProtectedRoute({ children, rolesPermitidos }) {
  const { usuario, verificando } = useAuth();

  // Todavía no confirmamos la sesión con el backend: no mostramos
  // nada protegido ni redirigimos, para evitar un "flash" incorrecto.
  if (verificando) {
    return (
      <div className="verificando-sesion">
        <span>Verificando sesión...</span>
      </div>
    );
  }

  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  if (rolesPermitidos && !rolesPermitidos.includes(usuario.rol)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
