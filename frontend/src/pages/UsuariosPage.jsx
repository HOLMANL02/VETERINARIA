import { useEffect, useState, useCallback } from "react";
import { listarUsuarios, crearUsuario } from "../api/usuarios";
import { listarRoles } from "../api/roles";

const FORM_VACIO = { nombre: "", correo: "", password: "", rol_id: "" };

export default function UsuariosPage() {
  const [usuarios, setUsuarios] = useState([]);
  const [roles, setRoles] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  const [modalAbierto, setModalAbierto] = useState(false);
  const [form, setForm] = useState(FORM_VACIO);
  const [guardando, setGuardando] = useState(false);
  const [errorModal, setErrorModal] = useState("");

  const cargar = useCallback(async () => {
    setCargando(true);
    setError("");
    try {
      const [datosUsuarios, datosRoles] = await Promise.all([
        listarUsuarios(),
        listarRoles(),
      ]);
      setUsuarios(datosUsuarios);
      setRoles(datosRoles);
    } catch {
      setError("No se pudieron cargar los usuarios.");
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    let activo = true;
    (async () => {
      await cargar();
      if (!activo) return;
    })();
    return () => {
      activo = false;
    };
  }, [cargar]);

  function nombreRol(rolId) {
    return roles.find((r) => r.id === rolId)?.nombre ?? "—";
  }

  function abrirCrear() {
    setForm({ ...FORM_VACIO, rol_id: roles[0]?.id ?? "" });
    setErrorModal("");
    setModalAbierto(true);
  }

  async function guardar(e) {
    e.preventDefault();
    setGuardando(true);
    setErrorModal("");
    try {
      await crearUsuario({ ...form, rol_id: Number(form.rol_id) });
      setModalAbierto(false);
      await cargar();
    } catch (err) {
      setErrorModal(
        err.response?.data?.detail ?? "No se pudo crear el usuario."
      );
    } finally {
      setGuardando(false);
    }
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Usuarios</h1>
          <p>Cuentas de acceso al sistema (personal interno).</p>
        </div>
        <button className="btn-primary" onClick={abrirCrear} disabled={cargando}>
          + Nuevo usuario
        </button>
      </div>

      {error && <div className="error-box">{error}</div>}

      <div className="card">
        {cargando ? (
          <div className="empty-state">Cargando usuarios...</div>
        ) : usuarios.length === 0 ? (
          <div className="empty-state">No hay usuarios registrados.</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((u) => (
                <tr key={u.id}>
                  <td>{u.nombre}</td>
                  <td>{u.correo}</td>
                  <td style={{ textTransform: "capitalize" }}>{nombreRol(u.rol_id)}</td>
                  <td>{u.estado ? "Activo" : "Inactivo"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {modalAbierto && (
        <div className="modal-backdrop" onClick={() => setModalAbierto(false)}>
          <form
            className="card modal"
            onClick={(e) => e.stopPropagation()}
            onSubmit={guardar}
          >
            <h2>Nuevo usuario</h2>

            {errorModal && <div className="error-box">{errorModal}</div>}

            <div className="field">
              <label htmlFor="nombre">Nombre completo</label>
              <input
                id="nombre"
                value={form.nombre}
                onChange={(e) => setForm({ ...form, nombre: e.target.value })}
                required
                autoFocus
              />
            </div>

            <div className="field">
              <label htmlFor="correo">Correo</label>
              <input
                id="correo"
                type="email"
                value={form.correo}
                onChange={(e) => setForm({ ...form, correo: e.target.value })}
                required
              />
            </div>

            <div className="field">
              <label htmlFor="password">Contraseña temporal</label>
              <input
                id="password"
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
                minLength={8}
              />
            </div>

            <div className="field">
              <label htmlFor="rol_id">Rol</label>
              <select
                id="rol_id"
                value={form.rol_id}
                onChange={(e) => setForm({ ...form, rol_id: e.target.value })}
                required
              >
                {roles.map((rol) => (
                  <option key={rol.id} value={rol.id}>
                    {rol.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div className="modal-actions">
              <button
                type="button"
                className="btn-secondary"
                onClick={() => setModalAbierto(false)}
              >
                Cancelar
              </button>
              <button className="btn-primary" type="submit" disabled={guardando}>
                {guardando ? "Guardando..." : "Guardar"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
