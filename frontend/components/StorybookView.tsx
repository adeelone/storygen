"use client";

import { Story } from "../lib/types";
import { SceneCard } from "./SceneCard";

export function StorybookView({ story }: { story: Story }) {
  function narrate() {
    const text = story.scenes.flatMap((scene) => scene.paragraphs).join(" ");
    speechSynthesis.speak(new SpeechSynthesisUtterance(text));
  }
  return (
    <main className="book">
      <header className="book-cover">
        <p>A StoryGen original</p>
        <h1>{story.plan?.title ?? story.slug}</h1>
        <button className="primary compact" onClick={narrate}>
          Narrate aloud
        </button>
      </header>
      {story.scenes.map((scene) => (
        <SceneCard scene={scene} key={scene.outline.number} />
      ))}
    </main>
  );
}
