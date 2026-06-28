"use client";

import { useState, KeyboardEvent } from "react";

interface IdeaInputProps {
  onAnalyze: (ideas: string[]) => void;
  isLoading: boolean;
}

export function IdeaInput({ onAnalyze, isLoading }: IdeaInputProps) {
  const [raw, setRaw] = useState("");

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !isLoading) {
      e.preventDefault();
      submit();
    }
  };

  const submit = () => {
    const ideas = raw
      .split(/[,\n;]+/)
      .map((s) => s.trim())
      .filter(Boolean)
      .slice(0, 5);

    if (ideas.length === 0) return;
    onAnalyze(ideas);
  };

  const ideas = raw
    .split(/[,\n;]+/)
    .map((s) => s.trim())
    .filter(Boolean);

  const overLimit = ideas.length > 5;
  const tooLong = ideas.some((s) => s.length > 200);
  const disabled = isLoading || ideas.length === 0 || overLimit || tooLong;

  return (
    <div className="w-full max-w-2xl mx-auto space-y-4">
      {/* Hero */}
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold tracking-tight text-white">
          What should you build?
        </h1>
        <p className="text-gray-400 text-base">
          Enter 1–5 business ideas. Get scored rankings — in 60 seconds.
        </p>
      </div>

      {/* Input card */}
      <div className="bg-[hsl(222,47%,8%)] border border-[hsl(217,33%,17%)] rounded-2xl p-6 space-y-4">
        <textarea
          value={raw}
          onChange={(e) => setRaw(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="AI tool for lawyers, SaaS for plumbers, Pet-sitting marketplace..."
          rows={4}
          disabled={isLoading}
          className="w-full bg-[hsl(222,47%,5%)] text-white placeholder-gray-500 rounded-lg px-4 py-3 text-sm resize-none outline-none focus:ring-2 focus:ring-indigo-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        />

        {/* Validation hints */}
        <div className="flex items-center justify-between text-xs">
          <div className="flex gap-3">
            {ideas.length > 0 && (
              <span className={overLimit ? "text-red-400" : "text-gray-500"}>
                {ideas.length}/5 ideas
              </span>
            )}
            {tooLong && <span className="text-red-400">Some ideas exceed 200 characters</span>}
          </div>
          <span className="text-gray-600 text-xs">Comma, newline, or semicolon separated</span>
        </div>

        {/* Analyze button */}
        <button
          onClick={submit}
          disabled={disabled}
          className="w-full py-3 rounded-lg font-semibold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed
            bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white
            flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <span className="animate-spin">◌</span>
              Analyzing...
            </>
          ) : (
            "Analyze"
          )}
        </button>
      </div>
    </div>
  );
}