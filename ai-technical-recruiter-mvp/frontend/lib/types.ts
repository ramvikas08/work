export type ScanPlan = "single" | "pro";

export interface ScanRequest {
  github_url: string;
  plan: ScanPlan;
}

export interface RepositoryScore {
  name: string;
  url: string;
  language?: string | null;
  stars: number;
  quality_score: number;
  consistency_score: number;
  complexity_score: number;
}

export interface ScanResult {
  scan_id: string;
  status: "completed";
  pdf_path: string;
  overall_score: number;
  quality_score: number;
  consistency_score: number;
  complexity_score: number;
  repositories: RepositoryScore[];
  summary: string;
}
