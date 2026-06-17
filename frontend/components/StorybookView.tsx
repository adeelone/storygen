"use client";

import { Story } from "../lib/types";
import { narrationUrl } from "../lib/api";
import { SceneCard } from "./SceneCard";

export function StorybookView({ story }: { story: Story }) {
  function narrate() {
    new Audio(narrationUrl(story.id)).play();
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
