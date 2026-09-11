import client from "./client";

export async function listarUsuarios() {
  const { data } = await client.get("/users");
  return data;
}

export async function crearUsuario(datos) {
  const { data } = await client.post("/users", datos);
  return data;
}
