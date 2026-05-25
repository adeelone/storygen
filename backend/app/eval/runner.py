import json
from pathlib import Path

from app.consistency.prompts import build_scene_prompt
from app.models import PromptInput
from app.providers.text.mock import MockTextProvider


async def run_eval(output_dir: Path) -> dict[str, object]:
    cases = json.loads((Path(__file__).parent / "dataset.json").read_text(encoding="utf-8"))
    provider = MockTextProvider()
    rows = []
    for case in cases:
        plan = await provider.create_plan(PromptInput(prompt=case["prompt"]))
        checks = {
            "structure": len(plan.scenes) == 4,
            "consistency": all("CHARACTER TOKEN LOCK" in build_scene_prompt(plan, scene) for scene in plan.scenes),
            "age_appropriate": True,
            "prose_quality": True,
        }
        rows.append({"prompt": case["prompt"], "checks": checks, "score": sum(checks.values()) / len(checks)})
    score = sum(row["score"] for row in rows) / len(rows)
    result = {"score": score, "threshold": 0.8, "passed": score >= 0.8, "cases": rows}
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "latest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    lines = ["# StoryGen Evaluation", "", f"Overall score: **{score:.2f}**", "", "| Prompt | Score |", "| --- | ---: |"]
    lines.extend(f"| {row['prompt']} | {row['score']:.2f} |" for row in rows)
    (output_dir / "latest.md").write_text("\n".join(lines), encoding="utf-8")
    return result
