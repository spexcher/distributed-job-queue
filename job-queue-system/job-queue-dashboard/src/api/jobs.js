import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000", // later: deployed URL
});

export const fetchJobs = (status) =>
  API.get("/jobs", { params: status ? { status } : {} });

export const fetchStats = () =>
  API.get("/jobs/stats");

export const fetchWorkers = () =>
  API.get("/jobs/workers");
