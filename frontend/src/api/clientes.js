import client from "./client";

export async function listarClientes(buscar = "") {
  const { data } = await client.get("/clients", {
    params: buscar ? { buscar } : {},
  });
  return data;
}

export async function crearCliente(datos) {
  const { data } = await client.post("/clients", datos);
  return data;
}

export async function actualizarCliente(id, datos) {
  const { data } = await client.put(`/clients/${id}`, datos);
  return data;
}

export async function eliminarCliente(id) {
  await client.delete(`/clients/${id}`);
}
