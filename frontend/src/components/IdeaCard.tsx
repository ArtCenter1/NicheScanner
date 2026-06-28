"use client";

import { IdeaScore } from "@/lib/api";

interface IdeaCardProps {
  idea: IdeaScore;
  rank: number;
}

const DIMENSION_LABELS: Record<keyof IdeaScore["dimensions"], string> = {
  supply_quality: "Supply Quality",
  demand_heat: "Demand Heat",
  business_viability: "Viability",
  timing: "Timing",
};

function ScoreBar({ value, label }: { value: number; label: string }) {
  const color =
    value >= 70 ? "bg-emerald-500" : value >= 50 ? "bg-amber-500" : "bg-red-500";

  return (
    <div className="flex items-center gap-3 text-sm">
      <span className="text-gray-400 w-28 text-xs shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-[hsl(222,47%,5%)] rounded-full overflow-hidden">
        <div className={color + " h-full rounded-full transition-all duration-700"} style={{ width: `${value}%` }} />
      </div>
      <span className="text-gray-400 w-8 text-right text-xs tabular-nums">{value}</span>
    </div>
  );
}

function SignalBadge({ label, available, detail }: { label: string; available: boolean; detail?: string }) {
  return (
    <span
      className={`text-xs px-2 py-0.5 rounded-full ${
        available
          ? "bg-emerald-500/10 text-emerald-400"
          : "bg-gray-700/50 text-gray-500"
      }`}
      title={available ? detail : "Data unavailable"}
    >
      {label}
    </span>
  );
}

function getScoreColor(score: number): string {
  if (score >= 75) return "text-emerald-400";
  if (score >= 55) return "text-amber-400";
  return "text-red-400";
}

export function IdeaCard({ idea, rank }: IdeaCardProps) {
  const scoreColor = getScoreColor(idea.total_score);

  return (
    <div className="bg-[hsl(222,47%,8%)] border border-[hsl(217,33%,17%)] rounded-xl p-5 hover:border-[hsl(239,84%,67%/30%)] transition-colors">
      {/* Header: rank + name + score */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-xl font-bold text-gray-600">#{rank}</span>
          <h3 className="text-white font-semibold text-base leading-tight">{idea.name}</h3>
        </div>
        <div className="text-right shrink-0 ml-4">
          <span className={`text-3xl font-bold tabular-nums ${scoreColor}`}>
            {idea.total_score}
          </span>
          <span className="text-gray-500 text-sm"> / 100</span>
        </div>
      </div>

      {/* Score bars */}
      <div className="space-y-2 mb-4">
        {(Object.keys(DIMENSION_LABELS) as Array<keyof IdeaScore["dimensions"]>).map((key) => (
          <ScoreBar
            key={key}
            value={idea.dimensions[key]}
            label={DIMENSION_LABELS[key]}
          />
        ))}
      </div>

      {/* Recommendation */}
      {idea.recommendation && (
        <blockquote className="bg-[hsl(222,47%,5%)] rounded-lg p-3 text-sm text-gray-300 leading-relaxed mb-4">
          💡 {idea.recommendation}
        </blockquote>
      )}

      {/* Signal sources */}
      <div className="flex flex-wrap gap-2">
        <SignalBadge
          label="Reddit"
          available={idea.signals.reddit.available}
          detail={idea.signals.reddit.post_count != null ? `${idea.signals.reddit.post_count} posts` : undefined}
        />
        <SignalBadge
          label="Trends"
          available={idea.signals.trends.available}
          detail={idea.signals.trends.direction}
        />
        <SignalBadge
          label="Product Hunt"
          available={idea.signals.producthunt.available}
          detail={idea.signals.producthunt.competitor_count != null ? `${idea.signals.producthunt.competitor_count} competitors` : undefined}
        />
      </div>
    </div>
  );
}