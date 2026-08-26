import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getTwinState = async () => {
    const response = await api.get("/api/twin/state");
    return response.data;
};

export const getStations = async () => {
    const response = await api.get("/api/twin/stations");
    return response.data;
};

export const getVehicles = async () => {
    const response = await api.get("/api/twin/vehicles");
    return response.data;
};

export const getBuffers = async () => {
    const response = await api.get("/api/twin/buffers");
    return response.data;
};

export const getMetrics = async () => {
    const response = await api.get("/api/twin/metrics");
    return response.data;
};

// export const getGraph = async () => {
//     const response = await api.get("/api/twin/graph");
//     return response.data;
// };

export const startTwin = async () => {
    const response = await api.post("/api/twin/start");
    return response.data;
};

export const stopTwin = async () => {
    const response = await api.post("/api/twin/stop");
    return response.data;
};

export const runWhatIf = async (scenario) => {
    const response = await api.post(
        "/api/twin/what-if",
        scenario
    );

    return response.data;
};

export const getProcessGraph = async () => {
  const response = await api.get("/api/twin/graph");
  return response.data;
};

export default api;