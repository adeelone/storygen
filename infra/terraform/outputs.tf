output "frontend_url" { value = google_cloud_run_v2_service.frontend.uri }
output "backend_url" { value = google_cloud_run_v2_service.backend.uri }
output "asset_bucket" { value = google_storage_bucket.assets.name }
output "redis_host" {
  value     = google_redis_instance.sessions.host
  sensitive = true
}
