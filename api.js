import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// ---------------- Auth ----------------
export const registerUser = (payload) => api.post("/auth/register", payload);
export const loginUser = (payload) => api.post("/auth/login", payload);
export const getProfile = () => api.get("/auth/profile");

// ---------------- Loans ----------------
export const createLoan = (payload) => api.post("/loan", payload);
export const listLoans = () => api.get("/loan");
export const getLoan = (id) => api.get(`/loan/${id}`);
export const updateLoan = (id, payload) => api.put(`/loan/${id}`, payload);
export const deleteLoan = (id) => api.delete(`/loan/${id}`);

// ---------------- Financial ----------------
export const runFinancialAnalysis = (payload) => api.post("/financial-analysis", payload);
export const getDashboard = () => api.get("/dashboard");
export const getAnalytics = () => api.get("/analytics");

// ---------------- Settlement ----------------
export const createSettlement = (loan_id) => api.post("/settlement", { loan_id });
export const getSettlement = (id) => api.get(`/settlement/${id}`);

// ---------------- Letters ----------------
export const generateLetter = (payload) => api.post("/generate-letter", payload);
export const getLetter = (id) => api.get(`/letters/${id}`);

// ---------------- History ----------------
export const listHistory = () => api.get("/history");
export const getHistoryEntry = (id) => api.get(`/history/${id}`);

export default api;
