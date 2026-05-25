"use client";

import { useEffect, useMemo } from "react";
import Image from "next/image";
import { websocketUrl } from "../lib/api";
import { useStoryStore } from "../lib/storyStore";
import { StreamEvent } from "../lib/types";
import { SceneCard } from "./SceneCard";

export function StoryStream() {
  const { story, characters, scenes, status, error, accept } = useStoryStore();
  const storyId = story?.id;
  const storyStatus = story?.status;

  useEffect(() => {
    if (!storyId || storyStatus === "complete") return;
    const socket = new WebSocket(websocketUrl(storyId));
    socket.onmessage = (message) =>
      accept(JSON.parse(message.data) as StreamEvent);
    return () => socket.close();
  }, [storyId, storyStatus, accept]);

  const ordered = useMemo(
    () =>
      Object.values(scenes).sort((a, b) => a.outline.number - b.outline.number),
    [scenes],
  );

  function cancel() {
    // A short-lived connection is sufficient because the server maintains session events for resume.
    const socket = new WebSocket(websocketUrl(story!.id));
    socket.onopen = () => socket.send(JSON.stringify({ type: "cancel" }));
  }

  async function reroll(scene: number) {
    const tweak = window.prompt(
      "Small illustration tweak",
      "add a few golden fireflies",
    );
    if (!tweak || !story) return;
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/v1/stories/${story.id}/scenes/${scene}/image`,
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ tweak }),
      },
    );
    accept({ type: "story_complete", data: { story: await response.json() } });
  }

  async function regenerate(scene: number) {
    if (!story) return;
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/v1/stories/${story.id}/scenes/${scene}/regenerate`,
      { method: "POST" },
    );
    accept({ type: "story_complete", data: { story: await response.json() } });
  }

  if (!story)
    return (
      <div className="empty-story">
        Your illustrated pages will assemble here.
      </div>
    );
  return (
    <section className="stream" aria-live="polite">
      <div className="stream-heading">
        <div>
          <p className="eyebrow">
            {status === "complete" ? "Story complete" : "Assembling your story"}
          </p>
          <h2>{story.plan?.title ?? "A new story is stirring..."}</h2>
        </div>
        {status !== "complete" ? (
          <button className="quiet" onClick={cancel}>
            Cancel
          </button>
        ) : null}
      </div>
      {story.plan ? (
        <p className="world">
          {story.plan.world.setting} - {story.plan.world.tone}
        </p>
      ) : null}
      <div className="characters">
        {characters.map((character) => (
          <figure key={character.id}>
            {character.reference_url ? (
              <Image
                src={`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}${character.reference_url}`}
                alt={`${character.name} reference`}
                width={96}
                height={96}
                unoptimized
              />
            ) : null}
            <figcaption>{character.name}</figcaption>
          </figure>
        ))}
      </div>
      {error ? <div className="friendly-error">{error}</div> : null}
      <div className="scenes">
        {ordered.map((scene) => (
          <SceneCard
            scene={scene}
            key={scene.outline.number}
            onReroll={reroll}
            onRegenerate={regenerate}
          />
        ))}
      </div>
    </section>
  );
}
