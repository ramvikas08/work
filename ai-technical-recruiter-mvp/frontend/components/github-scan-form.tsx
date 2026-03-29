"use client";

import { Search } from "lucide-react";
import { useState } from "react";

import { queueScan } from "@/lib/api";
import type { ScanPlan, ScanResult } from "@/lib/types";

export function GithubScanForm() {
  const [url, setUrl] = useState("");
  const [plan, setPlan] = useState<ScanPlan>("single");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ScanResult | null>(null);

  return (
    <div className="space-y-4">
      <form
        className="mx-auto flex w-full max-w-3xl flex-col gap-3 md:flex-row"
        onSubmit={async (event) => {
          event.preventDefault();
          setLoading(true);
          setError(null);
          try {
            const data = await queueScan({ github_url: url, plan });
            setResult(data);
          } catch (err) {
            setError(err instanceof Error ? err.message : "Unable to run scan");
          } finally {
            setLoading(false);
          }
        }}
      >
        <div className="flex flex-1 items-center rounded-xl border border-slate-700 bg-slate-900 px-3">
          <Search className="mr-2 h-4 w-4 text-slate-400" />
          <input
            className="w-full bg-transparent py-3 text-sm outline-none placeholder:text-slate-500"
            placeholder="https://github.com/username"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            required
          />
        </div>

        <select
          className="rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 text-sm"
          value={plan}
          onChange={(event) => setPlan(event.target.value as ScanPlan)}
        >
          <option value="single">Single Scan — $19</option>
          <option value="pro">Pro Monthly — $99</option>
        </select>

        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-black hover:bg-emerald-400 disabled:opacity-60"
        >
          {loading ? "Scanning..." : "Scan Candidate"}
        </button>
      </form>

      {error && <p className="text-sm text-rose-400">{error}</p>}

      {result && (
        <section className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <h2 className="text-xl font-semibold">Scorecard Ready</h2>
          <p className="mt-1 text-sm text-slate-300">Overall Score: {result.overall_score}/10</p>
          <p className="text-sm text-slate-300">PDF Path: {result.pdf_path}</p>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            {result.repositories.map((repo) => (
              <li key={repo.url} className="rounded-lg bg-slate-800/70 p-2">
                <strong>{repo.name}</strong> — Complexity {repo.complexity_score}/10
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
