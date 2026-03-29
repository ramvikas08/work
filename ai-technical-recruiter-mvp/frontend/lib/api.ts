import type { ScanRequest, ScanResult } from "./types";

export async function queueScan(payload: ScanRequest): Promise<ScanResult> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/scan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Scan failed");
  }

  return response.json() as Promise<ScanResult>;
}
