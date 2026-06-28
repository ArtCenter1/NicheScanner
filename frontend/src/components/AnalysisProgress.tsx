"use client";

import { IdeaScore } from "@/lib/api";

interface AnalysisProgressProps {
  phaseIndex: number;
}

export function AnalysisProgress({ phaseIndex }: AnalysisProgressProps) {
  const phases = [
    "Scraping Reddit, Product Hunt, and Google Trends...",
    "Computing scores...",
    "Generating recommendations...",
  ];

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="bg-[hsl(222,47%,8%)] border border-[hsl(217,33%,17%)] rounded-2xl p-6">
        <div className="space-y-3">
          {phases.map((phase, i) => {
            const done = i < phaseIndex;
            const active = i === phaseIndex;
            return (
              <div key={phase} className="flex items-center gap-3 text-sm">
                {done ? (
                  <span className="text-emerald-400 text-base">✓</span>
                ) : active ? (
                  <span className="text-indigo-400 animate-pulse">◌</span>
                ) : (
                  <span className="text-gray-600 text-base">○</span>
                )}
                <span className={done ? "text-gray-500 line-through" : active ? "text-white font-medium" : "text-gray-600"}>
                  {phase}
                </span>
              </div>
            );
          })}
        </div>

        {/* Progress bar */}
        <div className="mt-4 h-1.5 bg-[hsl(222,47%,5%)] rounded-full overflow-hidden">
          <div
            className="h-full bg-indigo-500 transition-all duration-500 rounded-full"
            style={{ width: `${((phaseIndex + 1) / phases.length) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
}

interface SkeletonCardProps {
  count: number;
}

export function ResultsSkeleton({ count }: SkeletonCardProps) {
  return (
    <div className="w-full max-w-2xl mx-auto space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="bg-[hsl(222,47%,8%)] border border-[hsl(217,33%,17%)] rounded-xl p-5 animate-pulse"
        >
          <div className="flex items-start justify-between mb-3">
            <div className="h-5 bg-[hsl(217,33%,12%)] rounded w-48" />
            <div className="h-8 bg-[hsl(217,33%,12%)] rounded w-12" />
          </div>
          <div className="space-y-2">
            {[80, 60, 40, 55].map((w, j) => (
              <div key={j} className="flex items-center gap-3">
                <div className="h-2 bg-[hsl(217,33%,12%)] rounded w-24" />
                <div className="h-2 bg-[hsl(217,33%,12%)] rounded" style={{ width: `${w}%` }} />
              </div>
            ))}
          </div>
          <div className="mt-4 h-3 bg-[hsl(217,33%,12%)] rounded w-full" />
        </div>
      ))}
    </div>
  );
}