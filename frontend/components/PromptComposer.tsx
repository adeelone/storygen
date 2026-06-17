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
  const [protagonists, setProtagonists] = useState("Lumi");
  const [setting, setSetting] = useState(
    "a firefly meadow beside a sleepy village",
  );
  const [vibe, setVibe] = useState("adventurous");
  const [ageBand, setAgeBand] = useState("5-7");
  const [length, setLength] = useState("standard");
  const [moral, setMoral] = useState("");
  const [language, setLanguage] = useState("English");
  const [aspectRatio, setAspectRatio] = useState("3:4");
  const [stylePreset, setStylePreset] = useState("watercolor");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      begin(
        await createStory({
          prompt,
          keywords,
          protagonists: guided
            ? protagonists
                .split(",")
                .map((value) => value.trim())
                .filter(Boolean)
            : [],
          setting: guided ? setting : undefined,
          vibe,
          age_band: ageBand,
          length,
          moral: moral || undefined,
          language,
          aspect_ratio: aspectRatio,
          style_preset: stylePreset,
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
        {guided ? "Hide guided fields" : "Use guided story settings"}
      </button>
      {guided ? (
        <div className="guided-grid">
          <label>
            Protagonists
            <input
              value={protagonists}
              onChange={(event) => setProtagonists(event.target.value)}
            />
          </label>
          <label>
            Setting
            <input
              value={setting}
              onChange={(event) => setSetting(event.target.value)}
            />
          </label>
          <label>
            Vibe
            <select
              value={vibe}
              onChange={(event) => setVibe(event.target.value)}
            >
              <option value="cozy">Cozy</option>
              <option value="adventurous">Adventurous</option>
              <option value="silly">Silly</option>
              <option value="bedtime">Bedtime</option>
            </select>
          </label>
          <label>
            Age
            <select
              value={ageBand}
              onChange={(event) => setAgeBand(event.target.value)}
            >
              <option value="3-5">3-5</option>
              <option value="5-7">5-7</option>
              <option value="7-9">7-9</option>
            </select>
          </label>
          <label>
            Length
            <select
              value={length}
              onChange={(event) => setLength(event.target.value)}
            >
              <option value="short">Short</option>
              <option value="standard">Standard</option>
              <option value="long">Long</option>
            </select>
          </label>
          <label>
            Language
            <select
              value={language}
              onChange={(event) => setLanguage(event.target.value)}
            >
              <option value="English">English</option>
              <option value="Spanish">Spanish</option>
            </select>
          </label>
          <label>
            Picture shape
            <select
              value={aspectRatio}
              onChange={(event) => setAspectRatio(event.target.value)}
            >
              <option value="1:1">Square cards</option>
              <option value="16:9">Wide scenes</option>
              <option value="3:4">Storybook pages</option>
            </select>
          </label>
          <label>
            Style
            <select
              value={stylePreset}
              onChange={(event) => setStylePreset(event.target.value)}
            >
              <option value="watercolor">Watercolor</option>
              <option value="gouache">Gouache</option>
              <option value="paper-cut">Paper cut</option>
            </select>
          </label>
          <label className="full">
            Moral or theme
            <input
              value={moral}
              onChange={(event) => setMoral(event.target.value)}
              placeholder="optional"
            />
          </label>
        </div>
      ) : null}
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
