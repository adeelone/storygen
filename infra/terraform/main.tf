resource "random_id" "suffix" {
  byte_length = 3
}

resource "google_project_service" "apis" {
  for_each = toset([
    "aiplatform.googleapis.com",
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "redis.googleapis.com",
    "storage.googleapis.com",
    "secretmanager.googleapis.com",
    "texttospeech.googleapis.com"
  ])
  service            = each.value
  disable_on_destroy = false
}

resource "google_storage_bucket" "assets" {
  name                        = "${var.project_id}-storygen-assets-${random_id.suffix.hex}"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false
  cors {
    origin          = ["*"]
    method          = ["GET"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }
}

resource "google_sql_database_instance" "postgres" {
  name             = "storygen-postgres-${random_id.suffix.hex}"
  database_version = "POSTGRES_16"
  region           = var.region
  settings {
    tier              = var.database_tier
    availability_type = "ZONAL"
    disk_autoresize   = true
    backup_configuration { enabled = true }
  }
  deletion_protection = true
  depends_on          = [google_project_service.apis]
}

resource "google_sql_database" "app" {
  name     = "storygen"
  instance = google_sql_database_instance.postgres.name
}

resource "google_redis_instance" "sessions" {
  name           = "storygen-sessions"
  tier           = "BASIC"
  memory_size_gb = 1
  region         = var.region
  redis_version  = "REDIS_7_0"
  depends_on     = [google_project_service.apis]
}

resource "google_service_account" "backend" {
  account_id   = "storygen-backend"
  display_name = "StoryGen backend"
}

resource "google_project_iam_member" "vertex" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.backend.email}"
}

resource "google_project_iam_member" "tts" {
  project = var.project_id
  role    = "roles/cloudtts.user"
  member  = "serviceAccount:${google_service_account.backend.email}"
}

resource "google_storage_bucket_iam_member" "asset_writer" {
  bucket = google_storage_bucket.assets.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.backend.email}"
}

resource "google_cloud_run_v2_service" "backend" {
  name     = "storygen-backend"
  location = var.region
  template {
    service_account = google_service_account.backend.email
    containers {
      image = var.backend_image
      env { name = "APP_ENV" value = "production" }
      env { name = "GOOGLE_CLOUD_PROJECT" value = var.project_id }
      env { name = "TEXT_PROVIDER" value = "gemini" }
      env { name = "IMAGE_PROVIDER" value = "imagen" }
      env { name = "TTS_PROVIDER" value = "gcp" }
      env { name = "STORAGE_PROVIDER" value = "gcs" }
      env { name = "STORAGE_BUCKET" value = google_storage_bucket.assets.name }
      env { name = "REDIS_URL" value = "redis://${google_redis_instance.sessions.host}:6379/0" }
      env { name = "ADMIN_KEY" value = var.admin_key }
    }
  }
  depends_on = [google_project_service.apis]
}

resource "google_cloud_run_v2_service_iam_member" "backend_public" {
  count    = var.allow_public_backend ? 1 : 0
  name     = google_cloud_run_v2_service.backend.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_v2_service" "frontend" {
  name     = "storygen-frontend"
  location = var.region
  template {
    containers {
      image = var.frontend_image
      env { name = "NEXT_PUBLIC_API_URL" value = google_cloud_run_v2_service.backend.uri }
    }
  }
  depends_on = [google_project_service.apis]
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  count    = var.allow_public_frontend ? 1 : 0
  name     = google_cloud_run_v2_service.frontend.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}
