"use client";

import { useState, useEffect, useRef } from "react";
import { IdeaInput } from "@/components/IdeaInput";
import { AnalysisProgress, ResultsSkeleton } from "@/components/AnalysisProgress";
import { IdeaCard } from "@/components/IdeaCard";
import { ReportDownload } from "@/components/ReportDownload";
import type { AnalysisResponse, IdeaScore } from "@/lib/api";
import { submitAnalysis, pollAnalysis } from "@/lib/api";

const POLL_INTERVAL_MS = 1500;
const MAX_POLLS = 80;

type Phase = "idle" | "submitting" | "scraping" | "scoring" | "enriching" | "done" | "error";

function statusToPhase(status: string): Phase {
  switch (status) {
    case "pending":          return "scraping";
    case "scraping":         return "scraping";
    case "scoring":          return "scoring";
    case "enriching":        return "enriching";
    case "complete":
    case "partial":          return "done";
    case "failed":           return "error";
    default:                 return "idle";
  }
}

function phaseToIndex(phase: Phase): number {
  switch (phase) {
    case "scraping":  return 0;
    case "scoring":   return 1;
    case "enriching":  return 2;
    default:          return -1;
  }
}

export default function Home() {
  const [phase, setPhase] = useState<Phase>("idle");
  const [phaseIndex, setPhaseIndex] = useState(-1);
  const [results, setResults] = useState<IdeaScore[]>([]);
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const pollCount = useRef(0);

  // Polling loop
  useEffect(() => {
    if (!analysisId || phase !== "submitting") return;

    const timer = setInterval(async () => {
      pollCount.current += 1;

      try {
        const data: AnalysisResponse = await pollAnalysis(analysisId);

        if (data.status === "failed") {
          setPhase("error");
          setErrorMsg(data.error ?? "Analysis failed");
          clearInterval(timer);
          return;
        }

        const newPhase = statusToPhase(data.status);
        setPhase(newPhase);
        setPhaseIndex(phaseToIndex(newPhase));

        if (newPhase === "done") {
          setResults(data.ideas ?? []);
          clearInterval(timer);
          return;
        }

        if (pollCount.current >= MAX_POLLS) {
          setPhase("error");
          setErrorMsg("Analysis timed out. Please try again.");
          clearInterval(timer);
          return;
        }
      } catch {
        // Network error during poll — keep trying
      }
    }, POLL_INTERVAL_MS);

    return () => clearInterval(timer);
  }, [analysisId, phase]);

  const handleAnalyze = async (ideas: string[]) => {
    setPhase("submitting");
    setPhaseIndex(-1);
    setResults([]);
    setErrorMsg(null);
    pollCount.current = 0;

    try {
      const { analysis_id } = await submitAnalysis(ideas);
      setAnalysisId(analysis_id);
      setPhase("scraping");
      setPhaseIndex(0);
    } catch (err) {
      setPhase("error");
      setErrorMsg(err instanceof Error ? err.message : "Failed to start analysis");
    }
  };

  const handleRetry = () => {
    setPhase("idle");
    setPhaseIndex(-1);
    setResults([]);
    setAnalysisId(null);
    setErrorMsg(null);
  };

  // --- Render ---
  return (
    <div className="min-h-screen bg-[hsl(222,47%,5%)] text-white flex flex-col">
      <div className="w-full max-w-2xl mx-auto px-4 py-16 flex flex-col gap-8">

        {/* 1. Input */}
        <IdeaInput onAnalyze={handleAnalyze} isLoading={phase !== "idle" && phase !== "done" && phase !== "error"} />

        {/* 2. Progress (shown while analyzing) */}
        {(phase === "submitting" || phase === "scraping" || phase === "scoring" || phase === "enriching") && (
          <AnalysisProgress phaseIndex={phaseIndex} />
        )}

        {/* 3. Skeleton while transitioning to done */}
        {(phase === "enriching") && (
          <ResultsSkeleton count={3} />
        )}

        {/* 4. Error */}
        {phase === "error" && (
          <div className="bg-red-950/50 border border-red-800/30 rounded-xl p-5 text-center space-y-3">
            <p className="text-red-300 text-sm">{errorMsg ?? "Something went wrong."}</p>
            <button
              onClick={handleRetry}
              className="text-sm text-red-400 hover:text-red-300 underline"
            >
              Try again
            </button>
          </div>
        )}

        {/* 5. Results */}
        {phase === "done" && results.length > 0 && (
          <div className="space-y-3 animate-[fadeIn_0.3s_ease]">
            {/* Section header */}
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
                Ranked Results
              </h2>
              <span className="text-xs text-gray-600">{results.length} ideas analyzed</span>
            </div>

            {/* Cards */}
            <div className="space-y-3">
              {results.map((idea, i) => (
                <IdeaCard key={idea.name} idea={idea} rank={i + 1} />
              ))}
            </div>

            {/* PDF download */}
            {analysisId && (
              <ReportDownload analysisId={analysisId} status="complete" />
            )}

            {/* Reset */}
            <div className="text-center">
              <button
                onClick={handleRetry}
                className="text-sm text-gray-500 hover:text-gray-300 transition-colors"
              >
                Analyze new ideas →
              </button>
            </div>
          </div>
        )}
      </div>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}