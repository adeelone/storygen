# Infrastructure

Terraform provisions Cloud Run services, a private asset bucket, Cloud SQL,
Memorystore and a least-privilege backend service account. Configure the
application provider flags and secrets before sending production traffic.
The frontend and backend services are public by default because the browser
calls the backend API and WebSocket endpoint directly.

```bash
cd infra/terraform
terraform init
terraform apply -var="project_id=$GCP_PROJECT_ID" \
  -var="backend_image=$BACKEND_IMAGE" \
  -var="frontend_image=$FRONTEND_IMAGE" \
  -var="admin_key=$ADMIN_KEY"
```
