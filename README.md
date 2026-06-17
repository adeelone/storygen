# StoryGen

<!-- Badges: CI | Eval Gate | License | Cloud Run -->

**StoryGen turns a short prompt or guided form into a four-scene illustrated children's story.**

The app has a FastAPI backend, a Next.js frontend, WebSocket streaming, local deterministic providers for development, and optional Google Cloud provider adapters for deployments with credentials.

## Features

- Three input modes: free text, keyword chips, and a guided form.
- A four-act narrative plan with a world bible and explicit character sheets.
- Live WebSocket events for plans, reference sheets, prose, images and completion.
- Character consistency through reference-sheet renders, ordered token blocks, style locks and stable seeds.
- Library, full-page reader, share links, narration control, PDF and ePub endpoints.
- Friendly age-oriented screening, soft generation budgets and provider resilience primitives.
- Local development with deterministic providers, Docker Compose services and Terraform for Cloud Run.
- Reproducible evaluation suite with JSON and Markdown reports.

## Install

### Docker

Only Docker and one copied configuration file are needed for local development:

```bash
cp .env.example .env
docker compose up --build
```

Open `http://localhost:3000`. Cloud providers are disabled by default, so the first story does not require credentials.

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

The Terraform files provision Cloud Run, Cloud SQL, Memorystore and GCS. Set the provider variables and install the backend cloud extras before using Vertex AI or GCS in production.

## Assumptions

- Local development uses deterministic text, SVG image and WAV narration providers.
- `TEXT_PROVIDER=gemini`, `IMAGE_PROVIDER=imagen` and `STORAGE_PROVIDER=gcs` require Google Cloud credentials and `backend[cloud]`.
- Anonymous local stories are stored in a JSON file. Cloud SQL and Redis are provisioned by Terraform but not required for local runs.
- Content strictness is applied with rules; a cloud moderation provider can add richer classifications.

## Contributing

Read [CONTRIBUTING.md](./CONTRIBUTING.md), open an issue for meaningful product changes, and include tests and updated provider fixtures with behavior changes. Reports of security issues should follow [SECURITY.md](./SECURITY.md).

## License

MIT, copyright 2026 adeelone. See [LICENSE](./LICENSE).
