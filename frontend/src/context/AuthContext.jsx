import { useState, useCallback, useEffect } from "react";
import { login as loginRequest, obtenerUsuarioActual } from "../api/auth";
import { AuthContext } from "./authContextObject";

function decodificarPayload(token) {
  try {
    const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(atob(base64));
  } catch {
    return null;
  }
}

function payloadValido(token) {
  const payload = decodificarPayload(token);
  if (!payload) return null;
  if (payload.exp && payload.exp * 1000 < Date.now()) return null;
  return payload;
}

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [verificando, setVerificando] = useState(true);

  const confirmarSesion = useCallback(async (rolDelToken, { silencioso } = {}) => {
    try {
      const datos = await obtenerUsuarioActual();
      setUsuario({ ...datos, rol: rolDelToken });
    } catch (error) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      setUsuario(null);
      if (!silencioso) throw error;
    }
  }, []);

  useEffect(() => {
    let activo = true;
    (async () => {
      const token = localStorage.getItem("access_token");
      const payload = token ? payloadValido(token) : null;
      if (payload) {
        await confirmarSesion(payload.rol, { silencioso: true });
      }
      if (activo) setVerificando(false);
    })();
    return () => {
      activo = false;
    };
  }, [confirmarSesion]);

  const iniciarSesion = useCallback(
    async (correo, password) => {
      const data = await loginRequest(correo, password);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      const payload = payloadValido(data.access_token);
      await confirmarSesion(payload?.rol, { silencioso: false });
    },
    [confirmarSesion]
  );

  const cerrarSesion = useCallback(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUsuario(null);
  }, []);

  return (
    <AuthContext.Provider value={{ usuario, verificando, iniciarSesion, cerrarSesion }}>
      {children}
    </AuthContext.Provider>
  );
}