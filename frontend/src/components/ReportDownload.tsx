"use client";

import { useState } from "react";

interface ReportDownloadProps {
  analysisId: string;
  status: string;
}

export function ReportDownload({ analysisId, status }: ReportDownloadProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDownload = async () => {
    setIsLoading(true);
    setError(null);

    const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    const IS_MOCK = process.env.NEXT_PUBLIC_MOCK_API === "true";

    if (IS_MOCK) {
      setIsLoading(false);
      alert("PDF download is disabled in mock mode. Run the full backend to generate real reports.");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/api/v1/report/${analysisId}/pdf`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `niche-scanner-report-${analysisId.slice(0, 8)}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setError("PDF generation failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const canDownload = status === "complete" || status === "partial";

  if (!canDownload) return null;

  return (
    <div className="w-full max-w-2xl mx-auto">
      <button
        onClick={handleDownload}
        disabled={isLoading}
        className="w-full py-3 rounded-lg font-semibold text-sm transition-all flex items-center justify-center gap-2
          border border-indigo-500/30 text-indigo-300 hover:bg-indigo-500/10
          disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <>
            <span className="animate-spin">◌</span>
            Generating PDF...
          </>
        ) : (
          <>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            Download PDF Report
          </>
        )}
      </button>
      {error && (
        <p className="text-red-400 text-xs text-center mt-2">{error}</p>
      )}
    </div>
  );
}