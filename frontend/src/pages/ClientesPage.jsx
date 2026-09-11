import { useEffect, useState, useCallback } from "react";
import {
  listarClientes,
  crearCliente,
  actualizarCliente,
  eliminarCliente,
} from "../api/clientes";

const FORM_VACIO = { nombres: "", telefono: "", correo: "", direccion: "" };

export default function ClientesPage() {
  const [clientes, setClientes] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [buscar, setBuscar] = useState("");
  const [error, setError] = useState("");

  const [modalAbierto, setModalAbierto] = useState(false);
  const [clienteEditando, setClienteEditando] = useState(null); // null = creando
  const [form, setForm] = useState(FORM_VACIO);
  const [guardando, setGuardando] = useState(false);
  const [errorModal, setErrorModal] = useState("");

  const cargar = useCallback(async (textoBusqueda) => {
    setCargando(true);
    setError("");
    try {
      const data = await listarClientes(textoBusqueda);
      setClientes(data);
    } catch {
      setError("No se pudieron cargar los clientes.");
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    let activo = true;
    (async () => {
      await cargar("");
      if (!activo) return; // el componente ya se desmontó, no actualizamos estado
    })();
    return () => {
      activo = false;
    };
  }, [cargar]);

  function manejarBusqueda(e) {
    e.preventDefault();
    cargar(buscar);
  }

  function abrirCrear() {
    setClienteEditando(null);
    setForm(FORM_VACIO);
    setErrorModal("");
    setModalAbierto(true);
  }

  function abrirEditar(cliente) {
    setClienteEditando(cliente);
    setForm({
      nombres: cliente.nombres ?? "",
      telefono: cliente.telefono ?? "",
      correo: cliente.correo ?? "",
      direccion: cliente.direccion ?? "",
    });
    setErrorModal("");
    setModalAbierto(true);
  }

  async function guardar(e) {
    e.preventDefault();
    setGuardando(true);
    setErrorModal("");
    try {
      if (clienteEditando) {
        await actualizarCliente(clienteEditando.id, form);
      } else {
        await crearCliente(form);
      }
      setModalAbierto(false);
      await cargar(buscar);
    } catch (err) {
      setErrorModal(
        err.response?.data?.detail ?? "No se pudo guardar el cliente."
      );
    } finally {
      setGuardando(false);
    }
  }

  async function manejarEliminar(cliente) {
    const confirmar = window.confirm(
      `¿Eliminar a ${cliente.nombres}? Esta acción no se puede deshacer.`
    );
    if (!confirmar) return;

    try {
      await eliminarCliente(cliente.id);
      await cargar(buscar);
    } catch (err) {
      if (err.response?.status === 409) {
        alert("No se puede eliminar: este cliente tiene mascotas asociadas.");
      } else {
        alert("No se pudo eliminar el cliente.");
      }
    }
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Clientes</h1>
          <p>Propietarios y responsables de mascotas registrados.</p>
        </div>
        <button className="btn-primary" onClick={abrirCrear}>
          + Nuevo cliente
        </button>
      </div>

      <form onSubmit={manejarBusqueda} style={{ marginBottom: 16, maxWidth: 320 }}>
        <input
          placeholder="Buscar por nombre..."
          value={buscar}
          onChange={(e) => setBuscar(e.target.value)}
        />
      </form>

      {error && <div className="error-box">{error}</div>}

      <div className="card">
        {cargando ? (
          <div className="empty-state">Cargando clientes...</div>
        ) : clientes.length === 0 ? (
          <div className="empty-state">
            No hay clientes registrados todavía. Crea el primero con el botón de arriba.
          </div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Teléfono</th>
                <th>Correo</th>
                <th>Dirección</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {clientes.map((cliente) => (
                <tr key={cliente.id}>
                  <td>{cliente.nombres}</td>
                  <td>{cliente.telefono || "—"}</td>
                  <td>{cliente.correo || "—"}</td>
                  <td>{cliente.direccion || "—"}</td>
                  <td>
                    <div className="table-actions">
                      <button className="btn-secondary btn-sm" onClick={() => abrirEditar(cliente)}>
                        Editar
                      </button>
                      <button className="btn-danger btn-sm" onClick={() => manejarEliminar(cliente)}>
                        Eliminar
                      </button>
                    </div>
                  </td>
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
            <h2>{clienteEditando ? "Editar cliente" : "Nuevo cliente"}</h2>

            {errorModal && <div className="error-box">{errorModal}</div>}

            <div className="field">
              <label htmlFor="nombres">Nombre completo</label>
              <input
                id="nombres"
                value={form.nombres}
                onChange={(e) => setForm({ ...form, nombres: e.target.value })}
                required
                autoFocus
              />
            </div>

            <div className="field">
              <label htmlFor="telefono">Teléfono</label>
              <input
                id="telefono"
                value={form.telefono}
                onChange={(e) => setForm({ ...form, telefono: e.target.value })}
              />
            </div>

            <div className="field">
              <label htmlFor="correo">Correo</label>
              <input
                id="correo"
                type="email"
                value={form.correo}
                onChange={(e) => setForm({ ...form, correo: e.target.value })}
              />
            </div>

            <div className="field">
              <label htmlFor="direccion">Dirección</label>
              <input
                id="direccion"
                value={form.direccion}
                onChange={(e) => setForm({ ...form, direccion: e.target.value })}
              />
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
