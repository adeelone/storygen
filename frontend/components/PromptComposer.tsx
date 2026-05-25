"use client";

import { FormEvent, useState } from "react";
import { createStory } from "../lib/api";
import { useStoryStore } from "../lib/storyStore";

const suggestions = [
  "squirrel",
  "ocean",
  "treasure",
  "moonlight",
  "robot",
  "garden",
];

export function PromptComposer() {
  const begin = useStoryStore((state) => state.begin);
  const [prompt, setPrompt] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);
  const [guided, setGuided] = useState(false);
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      begin(
        await createStory({
          prompt,
          keywords,
          protagonists: guided ? ["Lumi"] : [],
          setting: guided
            ? "a firefly meadow beside a sleepy village"
            : undefined,
          vibe: guided ? "bedtime" : "adventurous",
          age_band: "5-7",
          language: "English",
          aspect_ratio: "3:4",
          style_preset: "watercolor",
        }),
      );
    } finally {
      setLoading(false);
    }
  }

  function toggleChip(chip: string) {
    setKeywords((values) =>
      values.includes(chip)
        ? values.filter((value) => value !== chip)
        : [...values, chip],
    );
  }

  return (
    <form className="composer" onSubmit={submit} aria-label="Create a story">
      <label htmlFor="idea">What should tonight&apos;s story be about?</label>
      <textarea
        id="idea"
        placeholder="A brave squirrel and her robot friend save the forest lights..."
        value={prompt}
        onChange={(event) => setPrompt(event.target.value)}
      />
      <div className="chips" aria-label="Story keywords">
        {suggestions.map((chip) => (
          <button
            className={keywords.includes(chip) ? "chip active" : "chip"}
            type="button"
            key={chip}
            onClick={() => toggleChip(chip)}
          >
            {chip}
          </button>
        ))}
      </div>
      <button
        className="guided-link"
        type="button"
        onClick={() => setGuided(!guided)}
      >
        {guided
          ? "Using bedtime guided settings"
          : "Use guided bedtime settings"}
      </button>
      <button
        className="primary"
        disabled={
          loading || (!prompt.trim() && keywords.length === 0 && !guided)
        }
      >
        {loading ? "Opening the book..." : "Create my story"}
      </button>
    </form>
  );
}
