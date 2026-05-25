# StoryGen

<!-- Badges: CI | Eval Gate | License | Cloud Run -->

**StoryGen turns a child's idea into a gentle four-scene illustrated story, assembled live on screen with consistent recurring characters.**

StoryGen is a polished, mobile-first storybook application built around real-time generation: an outline appears first, paragraphs stream into each page, and illustrations settle in around a locked character design and visual style. It runs immediately with deterministic mock providers and exposes clean adapter boundaries for Gemini, Imagen, text-to-speech, safety and object storage.

## Features

- Three input modes: free text, keyword chips, and guided bedtime settings.
- A four-act narrative plan with a world bible and explicit character sheets.
- Live WebSocket events for plans, reference sheets, prose, images and completion.
- Character consistency through reference-sheet renders, ordered token blocks, style locks and stable seeds.
- Library, full-page reader, share links, narration control, PDF and ePub endpoints.
- Friendly age-oriented screening, soft generation budgets and provider resilience primitives.
- Mock-first local development, Docker Compose services and Terraform Cloud Run scaffolding.
- Reproducible evaluation suite with JSON and Markdown reports.

## Install

### Docker

Only Docker and one copied configuration file are needed for the local mock-provider experience:

```bash
cp .env.example .env
docker compose up --build
```

Open `http://localhost:3000`. Cloud providers are disabled by default, so the first story requires no credentials.

### Bare Metal

Requires Python 3.12 and Node.js 20:

```bash
cp .env.example .env
python -m pip install -e "./backend[dev]"
cd frontend && npm install && cd ..
cd backend && uvicorn app.main:app --reload
# in another terminal
cd frontend && npm run dev
```

## Run And Test

```bash
make dev          # Docker application stack
make test         # pytest and Vitest
make lint         # Ruff/Black and ESLint
make typecheck    # mypy and TypeScript strict checks
make eval         # deterministic rubric report under backend/reports/
```

The frontend is at `http://localhost:3000`; API docs are at `http://localhost:8000/docs`.

## Environment Variables

Every supported variable is documented in [`.env.example`](./.env.example). The operational settings are:

| Area | Variables |
| --- | --- |
| Runtime | `APP_ENV`, `FRONTEND_URL`, `NEXT_PUBLIC_API_URL`, `DATABASE_URL`, `REDIS_URL` |
| AI | `TEXT_PROVIDER`, `IMAGE_PROVIDER`, `TTS_PROVIDER`, `SAFETY_PROVIDER`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GEMINI_MODEL`, `IMAGEN_MODEL` |
| Storage | `STORAGE_PROVIDER`, `STORAGE_BUCKET`, `STORAGE_ENDPOINT` |
| Controls | `SESSION_TOKEN_BUDGET`, `SESSION_IMAGE_BUDGET`, `ANONYMOUS_DAILY_QUOTA`, `SIGNED_URL_TTL_SECONDS` |
| Flags | `ENABLE_TTS`, `ENABLE_EVAL_DASHBOARD`, `ENABLE_PUBLIC_SHARING`, `ENABLE_PDF_EXPORT` |

Never commit `.env`, cloud credentials, state files or signed asset URLs.

## Project Structure

```text
backend/        FastAPI app, agents, provider contracts, consistency engine, eval and tests
frontend/       Next.js App Router UI, streaming state and component/browser tests
infra/terraform Cloud Run, GCS, Cloud SQL and Memorystore provisioning
.github/        Issue forms, automation and CI/evaluation/release workflows
```

See [ARCHITECTURE.md](./ARCHITECTURE.md), [PROVIDERS.md](./PROVIDERS.md), [CONSISTENCY.md](./CONSISTENCY.md), [EVAL.md](./EVAL.md), [DEPLOYMENT.md](./DEPLOYMENT.md), and [SECURITY.md](./SECURITY.md).

## Deployment

Build and push frontend and backend container images, then:

```bash
cd infra/terraform
terraform init
terraform apply -var="project_id=$GCP_PROJECT_ID" \
  -var="backend_image=$BACKEND_IMAGE" -var="frontend_image=$FRONTEND_IMAGE"
```

Cloud deployment scaffolding is present. Live Vertex generation and managed storage/cache/database adapters must be completed and load-tested before production traffic.

## Assumptions

- Local development prioritizes a zero-credential magical first run using deterministic story and SVG illustration providers.
- Google Gemini and Imagen are represented through stable adapter boundaries; the checked-in implementation intentionally falls back to local output until deployment credentials and Vertex calls are connected.
- SQLite/Postgres, Redis resume storage, GCS/MinIO signed URLs, OAuth, TTS audio, administrative trend persistence and high-fidelity PDF layout are production extension points rather than completed managed integrations in this initial release.
- Content strictness is applied to the youngest age band by rules; a cloud moderation provider can add richer classifications.

## Contributing

Read [CONTRIBUTING.md](./CONTRIBUTING.md), open an issue for meaningful product changes, and include tests and updated provider fixtures with behavior changes. Reports of security issues should follow [SECURITY.md](./SECURITY.md).

## License

MIT, copyright 2026 adeelone. See [LICENSE](./LICENSE).
