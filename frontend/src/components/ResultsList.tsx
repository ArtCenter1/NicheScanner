"use client";

import { IdeaCard } from "./IdeaCard";
import type { IdeaScore } from "@/lib/api";

interface ResultsListProps {
  ideas: IdeaScore[];
  analysisId: string | null;
}

export function ResultsList({ ideas, analysisId }: ResultsListProps) {
  return (
    <div className="space-y-3">
      {ideas.map((idea, i) => (
        <IdeaCard key={idea.name} idea={idea} rank={i + 1} />
      ))}
    </div>
  );
}