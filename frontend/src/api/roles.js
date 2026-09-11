import client from "./client";

export async function listarRoles() {
  const { data } = await client.get("/roles");
  return data;
}
