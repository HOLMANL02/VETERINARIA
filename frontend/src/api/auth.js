import client from "./client";

export async function login(correo, password) {
  const { data } = await client.post("/auth/login", { correo, password });
  return data; // { access_token, refresh_token, token_type }
}

export async function obtenerUsuarioActual() {
  const { data } = await client.get("/auth/me");
  return data; // { id, nombre, correo, rol_id, estado }
}
