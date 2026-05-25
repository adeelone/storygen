import { motion, useReducedMotion } from "framer-motion";
import Image from "next/image";
import { mediaUrl } from "../lib/api";
import { Scene } from "../lib/types";

export function SceneCard({
  scene,
  onReroll,
  onRegenerate,
}: {
  scene: Scene;
  onReroll?: (scene: number) => void;
  onRegenerate?: (scene: number) => void;
}) {
  const reduced = useReducedMotion();
  return (
    <motion.article
      className="scene"
      initial={reduced ? undefined : { opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <header>
        <span>{scene.outline.arc}</span>
        <h3>{scene.outline.title}</h3>
      </header>
      {scene.image_url ? (
        <motion.div
          initial={reduced ? undefined : { opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <Image
            src={mediaUrl(scene.image_url)!}
            alt={`Illustration for ${scene.outline.title}`}
            width={720}
            height={960}
            unoptimized
          />
        </motion.div>
      ) : (
        <div
          className="illustration-loading"
          aria-label="Illustration being painted"
        >
          Painting this scene...
        </div>
      )}
      <div className="prose">
        {scene.paragraphs.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
      </div>
      {scene.image_url && onReroll ? (
        <div className="scene-actions">
          <button
            className="quiet"
            onClick={() => onReroll(scene.outline.number)}
          >
            Adjust picture
          </button>
          {onRegenerate ? (
            <button
              className="quiet"
              onClick={() => onRegenerate(scene.outline.number)}
            >
              Regenerate scene
            </button>
          ) : null}
        </div>
      ) : null}
    </motion.article>
  );
}
