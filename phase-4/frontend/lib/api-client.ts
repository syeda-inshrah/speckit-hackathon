import axios, { AxiosInstance, AxiosError } from "axios";
import Cookies from "js-cookie";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = Cookies.get("auth_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to signin
      Cookies.remove("auth_token");
      Cookies.remove("user_id");
      if (typeof window !== "undefined") {
        window.location.href = "/signin";
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  signup: async (data: { email: string; password: string; name: string }) => {
    const response = await apiClient.post("/api/auth/signup", data);
    if (response.data.token) {
      Cookies.set("auth_token", response.data.token, { expires: 7 });
      Cookies.set("user_id", response.data.user.id, { expires: 7 });
    }
    return response.data;
  },

  signin: async (data: { email: string; password: string }) => {
    const response = await apiClient.post("/api/auth/signin", data);
    if (response.data.token) {
      Cookies.set("auth_token", response.data.token, { expires: 7 });
      Cookies.set("user_id", response.data.user.id, { expires: 7 });
    }
    return response.data;
  },

  signout: () => {
    Cookies.remove("auth_token");
    Cookies.remove("user_id");
    if (typeof window !== "undefined") {
      window.location.href = "/signin";
    }
  },

  getCurrentUser: () => {
    const token = Cookies.get("auth_token");
    const userId = Cookies.get("user_id");
    return token && userId ? { id: userId, token } : null;
  },
};

// Tasks API
export const tasksApi = {
  list: async (userId: string, status?: "all" | "pending" | "completed") => {
    const params = status ? { status } : {};
    const response = await apiClient.get(`/api/${userId}/tasks`, { params });
    return response.data;
  },

  create: async (userId: string, data: { title: string; description?: string }) => {
    const response = await apiClient.post(`/api/${userId}/tasks`, data);
    return response.data;
  },

  get: async (userId: string, taskId: number) => {
    const response = await apiClient.get(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  update: async (
    userId: string,
    taskId: number,
    data: { title?: string; description?: string }
  ) => {
    const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, data);
    return response.data;
  },

  toggleComplete: async (userId: string, taskId: number) => {
    const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`);
    return response.data;
  },

  delete: async (userId: string, taskId: number) => {
    const response = await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },
};

export default apiClient;
