const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const IS_MOCK = process.env.NEXT_PUBLIC_MOCK_API === "true";

/* ---------------------------------------------------------------------------
 * Backward-compat types — kept so old Polsia pages keep working.
 * --------------------------------------------------------------------------- */
export type ActivityEvent = {
  id: number;
  agent_type: string;
  action: string;
  summary: string;
  level: "info" | "success" | "warning" | "error";
  created_at: string;
};

export type DashboardSummary = {
  tasks_today_total: number;
  tasks_today_completed: number;
  tasks_today_pending: number;
  tasks_today_failed: number;
  active_agents: string[];
  kpis: Record<string, React.ReactNode>;
  last_report_date: string | null;
};

export type Task = {
  id: number;
  title: string;
  agent_type: string;
  status: string;
  priority: number;
  created_at: string;
};

export type AgentStatus = {
  agent_type: string;
  last_run_at: string | null;
  last_run_status: string | null;
  tasks_today: number;
  tasks_total: number;
};

export type FinanceSummary = {
  mrr_cents: number;
  arr_cents: number;
  active_subscribers: number;
  total_ad_spend_usd: number;
  total_expenses_month_cents: number;
  stripe_balance_cents: number;
  last_snapshot_date: string | null;
};

/* ---------------------------------------------------------------------------
 * Legacy Polsia API client — kept for backward compat with old pages.
 * --------------------------------------------------------------------------- */
const _LEGACY_API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const _LEGACY_API_KEY = process.env.NEXT_PUBLIC_API_KEY ?? "";

async function _legacyFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${_LEGACY_API_URL}/api/v1${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": _LEGACY_API_KEY,
      ...options.headers,
    },
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string) => _legacyFetch<T>(path),
  post: <T>(path: string, body?: unknown) =>
    _legacyFetch<T>(path, { method: "POST", body: JSON.stringify(body) }),
  put: <T>(path: string, body?: unknown) =>
    _legacyFetch<T>(path, { method: "PUT", body: JSON.stringify(body) }),
};

/* ---------------------------------------------------------------------------
 * Niche Scanner: shared API fetch helper
 * --------------------------------------------------------------------------- */
async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_URL}/api/v1${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

/* ---------------------------------------------------------------------------
 * Niche Scanner: types (must match backend / FRONTEND_HANDOFF.md)
 * --------------------------------------------------------------------------- */
export interface IdeaScore {
  name: string;
  total_score: number;
  dimensions: {
    supply_quality: number;
    demand_heat: number;
    business_viability: number;
    timing: number;
  };
  recommendation: string;
  signals: {
    reddit: { available: boolean; post_count?: number; avg_sentiment?: number };
    trends: { available: boolean; direction?: string; slope?: number };
    producthunt: { available: boolean; competitor_count?: number };
  };
}

export interface AnalysisResponse {
  status:
    | "pending"
    | "scraping"
    | "scoring"
    | "enriching"
    | "complete"
    | "partial"
    | "failed";
  analysis_id?: string;
  progress?: string;
  error?: string;
  ideas?: IdeaScore[];
}

/* ---------------------------------------------------------------------------
 * Niche Scanner: mock data (used when IS_MOCK=true or backend unreachable)
 * --------------------------------------------------------------------------- */
const MOCK_IDEAS: IdeaScore[] = [
  {
    name: "AI tool for lawyers",
    total_score: 78,
    dimensions: { supply_quality: 82, demand_heat: 74, business_viability: 65, timing: 88 },
    recommendation:
      "Start with a Chrome extension that summarizes legal documents. Law firms are actively seeking AI tools — the signal is strongest in demand heat and timing.",
    signals: {
      reddit: { available: true, post_count: 124, avg_sentiment: 0.6 },
      trends: { available: true, direction: "rising", slope: 0.15 },
      producthunt: { available: true, competitor_count: 3 },
    },
  },
  {
    name: "SaaS for plumbers",
    total_score: 52,
    dimensions: { supply_quality: 45, demand_heat: 60, business_viability: 70, timing: 35 },
    recommendation:
      "The market is less crowded but demand signals are weaker. Consider niche focus on scheduling + invoicing for independent plumbers.",
    signals: {
      reddit: { available: true, post_count: 38, avg_sentiment: 0.3 },
      trends: { available: false },
      producthunt: { available: true, competitor_count: 1 },
    },
  },
  {
    name: "Pet-sitting marketplace",
    total_score: 64,
    dimensions: { supply_quality: 58, demand_heat: 71, business_viability: 55, timing: 72 },
    recommendation:
      "Target urban pet owners first. A waitlist + pre-sell strategy reduces risk before you build scheduling software.",
    signals: {
      reddit: { available: true, post_count: 89, avg_sentiment: 0.5 },
      trends: { available: true, direction: "rising", slope: 0.08 },
      producthunt: { available: true, competitor_count: 2 },
    },
  },
];

/* ---------------------------------------------------------------------------
 * Niche Scanner: public API calls
 * --------------------------------------------------------------------------- */
export async function submitAnalysis(ideas: string[]): Promise<{ analysis_id: string }> {
  if (IS_MOCK) return { analysis_id: "mock-analysis-id" };
  return apiFetch("/analyze", { method: "POST", body: JSON.stringify({ ideas }) });
}

export async function pollAnalysis(analysisId: string): Promise<AnalysisResponse> {
  if (IS_MOCK) return { status: "complete", ideas: MOCK_IDEAS };
  return apiFetch(`/report/${analysisId}`);
}