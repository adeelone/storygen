import asyncio
from pathlib import Path

from app.eval.runner import run_eval


async def main() -> None:
    result = await run_eval(Path("reports"))
    print(f"Evaluation score: {result['score']:.2f}")
    raise SystemExit(0 if result["passed"] else 1)


asyncio.run(main())
