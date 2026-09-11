import axios from "axios";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Agrega el access_token a cada request saliente, si existe
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Si el backend responde 401 (token expirado), intenta refrescar
// la sesión UNA vez con el refresh_token antes de rendirse.
let refrescando = null;

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    const esLogin = original?.url?.includes("/auth/login");

    if (error.response?.status === 401 && !original._retry && !esLogin) {
      original._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        return Promise.reject(error);
      }

      try {
        // Evita disparar varios refresh en paralelo si varias
        // peticiones fallan al mismo tiempo.
        if (!refrescando) {
          refrescando = axios
            .post(`${import.meta.env.VITE_API_URL}/auth/refresh`, {
              refresh_token: refreshToken,
            })
            .finally(() => {
              refrescando = null;
            });
        }
        const { data } = await refrescando;
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        original.headers.Authorization = `Bearer ${data.access_token}`;
        return client(original);
      } catch (refreshError) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default client;
