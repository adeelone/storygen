# Deployment

## Local Compose

```bash
cp .env.example .env
docker compose up --build
```

This launches the frontend, backend and development Postgres, Redis and MinIO services. The default application providers remain deterministic local implementations.

## Cloud Run With Terraform

1. Create a Google Cloud project and enable billing.
2. Authenticate `gcloud`, configure Artifact Registry and build both container images.
3. Export `GCP_PROJECT_ID`, `BACKEND_IMAGE`, `FRONTEND_IMAGE` and a strong `ADMIN_KEY`.
4. Run `terraform init` and `terraform apply` in `infra/terraform`.
5. Set provider flags to managed modes and validate them with project credentials.

Terraform enables Vertex AI, Text-to-Speech, Cloud Run, Cloud SQL, Memorystore, Storage and Secret Manager services; provisions a GCS bucket, Postgres instance, Redis instance, two Cloud Run services and a restricted backend service account. Both frontend and backend Cloud Run services can be public because the browser calls the backend API and WebSocket endpoint directly.

## IAM And Secrets

The backend identity receives Vertex user and bucket object-writer roles. Pass `-var="admin_key=$ADMIN_KEY"` for the admin dashboard until Secret Manager wiring is added. Add database credentials and application secrets through Secret Manager rather than images. Keep Cloud SQL connectivity private for a production environment.

## Current Production Limitation

The app still uses the JSON repository implementation at runtime. Cloud SQL is provisioned for the production architecture, but `DATABASE_URL` is not yet consumed by the backend repository layer. Do not treat Cloud Run story persistence as durable until the repository is replaced with SQLAlchemy/Postgres or an equivalent managed store.

## Cost And Rollback

Cloud SQL and Memorystore introduce baseline costs even with no stories generated. Use budget alerts and lower-cost regional settings during evaluation. For rollback, redeploy a prior immutable container digest and revert Terraform changes only after reviewing retained data resources; storage and database deletion protection are deliberate.
