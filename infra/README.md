# Infrastructure

Terraform provisions Cloud Run services, a private asset bucket, Cloud SQL,
Memorystore and a least-privilege backend service account. Configure the
application provider flags and secrets before sending production traffic.

```bash
cd infra/terraform
terraform init
terraform apply -var="project_id=$GCP_PROJECT_ID" \
  -var="backend_image=$BACKEND_IMAGE" -var="frontend_image=$FRONTEND_IMAGE"
```
