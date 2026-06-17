# Providers

## Registry

| Capability | Local default | Intended managed adapter | Fallback |
| --- | --- | --- | --- |
| Text planning/prose | `MockTextProvider` | Gemini via Vertex AI | Mock text |
| Illustration | `MockImageProvider` | Imagen via Vertex AI | Text-only story |
| Safety | `RulesSafetyProvider` | Provider moderation plus rules | Rules |
| Narration | WAV tone preview | Google Cloud TTS | Disabled narration |
| Media storage | Local files | GCS signed URLs / MinIO development | Local media |

Local providers are deterministic and incur no network cost. Gemini, Imagen and GCS providers use Google SDKs when the cloud extras and credentials are installed.

## Adding A Provider

1. Implement the relevant interface in `backend/app/providers/<capability>/`.
2. Add one selection branch in that capability's `__init__.py` registry.
3. Add safe configuration keys in `.env.example`.
4. Add fixture-backed tests; CI must never call live services.
5. Document costs, safety behavior, retry and reference-conditioning capabilities here.

## Free Tier And Cost Notes

Local providers are free. Google Cloud model and storage pricing varies by region and model revision; confirm current Vertex AI, Cloud Run, Cloud SQL, Memorystore and GCS pricing during deployment rather than relying on static estimates.
