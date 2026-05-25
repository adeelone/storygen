# Infrastructure

Terraform provisions Cloud Run services, a private asset bucket, Cloud SQL,
Memorystore and a least-privilege backend service account. The runtime adapter
implementations for Cloud SQL, Memorystore and GCS are intentionally bounded
behind application interfaces; finish those adapters before exposing a
production deployment to users.

```bash
cd infra/terraform
terraform init
terraform apply -var="project_id=$GCP_PROJECT_ID" \
  -var="backend_image=$BACKEND_IMAGE" -var="frontend_image=$FRONTEND_IMAGE"
```
