export interface IntelligenceEvent {
  id: string;
  title: string;
  summary?: string;
  event_type: string;
  source_name: string;
  source_url: string;
  category_tags: string[];
  entities_mentioned: string[];
  relevant_body?: string;
  country?: string;
  city?: string;
  latitude?: number;
  longitude?: number;
  sentiment_score: number;
  impact_score: number;
  published_at?: string;
  collected_at?: string;
  extra: Record<string, unknown>;
}

export interface FinancialSnapshot {
  id: string;
  ticker: string;
  company_name: string;
  sector?: string;
  price?: number;
  open_price?: number;
  high?: number;
  low?: number;
  volume?: number;
  market_cap?: number;
  pe_ratio?: number;
  change_pct?: number;
  currency: string;
  exchange?: string;
  snapshot_at?: string;
}

export interface LiveStream {
  id: string;
  video_id: string;
  title: string;
  channel_name?: string;
  stream_url: string;
  thumbnail_url?: string;
  is_live: boolean;
  viewer_count: number;
  category_tags: string[];
  started_at?: string;
  collected_at?: string;
}

export interface ThreatIndicator {
  id: string;
  indicator_id: string;
  title: string;
  description?: string;
  indicator_type: string;
  severity?: string;
  cvss_score?: number;
  cvss_vector?: string;
  affected_products: string[];
  references: string[];
  cwe_ids: string[];
  tags: string[];
  source_name?: string;
  published_at?: string;
  modified_at?: string;
}

export interface CertificationUpdate {
  id: string;
  body_name: string;
  standard_id?: string;
  title: string;
  summary?: string;
  update_type?: string;
  source_url?: string;
  region?: string;
  published_at?: string;
}

export interface PaginatedResponse<T> {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: T[];
}

export interface DashboardStats {
  total: number;
  by_type: Record<string, number>;
  top_countries: Record<string, number>;
}

export interface MapEvent {
  id: string;
  title: string;
  latitude: number;
  longitude: number;
  event_type: string;
  impact_score: number;
  source_name: string;
  country?: string;
  published_at?: string;
}
