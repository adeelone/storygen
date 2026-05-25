# Deployment

## Local Compose

```bash
cp .env.example .env
docker compose up --build
```

This launches the frontend, backend and development Postgres, Redis and MinIO services. The default application adapters remain deterministic local implementations.

## Cloud Run With Terraform

1. Create a Google Cloud project and enable billing.
2. Authenticate `gcloud`, configure Artifact Registry and build both container images.
3. Export `GCP_PROJECT_ID`, `BACKEND_IMAGE` and `FRONTEND_IMAGE`.
4. Run `terraform init` and `terraform apply` in `infra/terraform`.
5. Implement and validate Vertex, GCS, Redis and Cloud SQL adapters, then set provider flags to managed modes.

Terraform enables Vertex AI, Cloud Run, Cloud SQL, Memorystore, Storage and Secret Manager services; provisions a GCS bucket, Postgres instance, Redis instance, two Cloud Run services and a restricted backend service account.

## IAM And Secrets

The backend identity receives Vertex user and bucket object-writer roles. Add database credentials and application secrets through Secret Manager rather than Terraform variables or images. Keep Cloud SQL connectivity private for a production environment.

## Cost And Rollback

Cloud SQL and Memorystore introduce baseline costs even with no stories generated. Use budget alerts and lower-cost regional settings during evaluation. For rollback, redeploy a prior immutable container digest and revert Terraform changes only after reviewing retained data resources; storage and database deletion protection are deliberate.
