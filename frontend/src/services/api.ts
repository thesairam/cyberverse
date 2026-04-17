import axios from "axios";
import type { IntelligenceEvent, FinancialSnapshot, LiveStream, ThreatIndicator, CertificationUpdate, PaginatedResponse, DashboardStats } from "@/types";

const http = axios.create({ baseURL: "/api/v1", timeout: 15000 });

export const intelligenceApi = {
  list(params?: Record<string, unknown>)  { return http.get<PaginatedResponse<IntelligenceEvent>>("/intelligence/", { params }); },
  top(n = 10)                             { return http.get<IntelligenceEvent[]>("/intelligence/top", { params: { n } }); },
  map(params?: Record<string, unknown>)   { return http.get<IntelligenceEvent[]>("/intelligence/map", { params }); },
  stats()                                 { return http.get<DashboardStats>("/intelligence/stats"); },
  sources()                               { return http.get<{ sources: { name: string; count: number }[] }>("/intelligence/sources"); },
};

export const financialApi = {
  list(sector?: string)                   { return http.get<FinancialSnapshot[]>("/financial/", { params: sector ? { sector } : {} }); },
  movers()                                { return http.get<{ gainers: FinancialSnapshot[]; losers: FinancialSnapshot[] }>("/financial/movers"); },
  history(ticker: string, limit = 30)     { return http.get<FinancialSnapshot[]>(`/financial/${ticker}/history`, { params: { limit } }); },
};

export const streamsApi = {
  list(live_only = false)                 { return http.get<LiveStream[]>("/streams/", { params: { live_only } }); },
};

export const threatsApi = {
  list(params?: Record<string, unknown>)  { return http.get<PaginatedResponse<ThreatIndicator>>("/threats/", { params }); },
  critical(limit = 20)                    { return http.get<ThreatIndicator[]>("/threats/critical", { params: { limit } }); },
};

export const certificationsApi = {
  list(params?: Record<string, unknown>)  { return http.get<PaginatedResponse<CertificationUpdate>>("/certifications/", { params }); },
  bodies()                                { return http.get<{ bodies: string[] }>("/certifications/bodies"); },
};
