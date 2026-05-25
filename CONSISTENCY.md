# Character Consistency

Illustration coherence is part of the pipeline contract, not a lucky property of an image model.

## Four Locks

1. **Reference sheet pass.** Each character receives a square design sheet before any scene: front view, three-quarter view and expression. Its stored URL can become reference-conditioning input for capable providers.
2. **Token lock.** Every scene prompt contains a fixed-order character block including species, appearance, palette, clothing, accessory and distinguishing mark.
3. **Style lock.** The plan owns one descriptor such as `soft watercolor children's-book illustration, gentle ink outlines, warm luminous light`; it appears verbatim in every rendered scene.
4. **Seed pinning.** `sha256(story_id:character_id)` supplies a deterministic seed, with the scene number offset for page variation.

## Worked Prompt Shape

```text
STYLE LOCK:
soft watercolor children's-book illustration, gentle ink outlines, warm luminous light.
CHARACTER TOKEN LOCK - do not alter these identifiers:
[Lumi] species=young squirrel; appearance=hazel eyes, warm chestnut fur; palette=chestnut, moss green; clothing=moss-green satchel; accessory=a tiny compass
COMPOSITION:
the whispering hilltop; Lumi lifts the lantern into the wind; emotional beat: courage together.
```

## Failure Modes

- Text-only prompting can drift with crowded group scenes; use reference-conditioning where supported.
- Deterministic seeds improve reproducibility but do not guarantee identity between model revisions.
- A reroll tweak may conflict with a token lock; token blocks must win.
- The bundled mock SVG provider demonstrates stable composition but is not an image-generation quality benchmark.
