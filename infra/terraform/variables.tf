variable "project_id" { type = string }
variable "region" {
  type    = string
  default = "us-central1"
}
variable "backend_image" { type = string }
variable "frontend_image" { type = string }
variable "database_tier" {
  type    = string
  default = "db-f1-micro"
}
variable "allow_public_frontend" {
  type    = bool
  default = true
}
variable "allow_public_backend" {
  type    = bool
  default = true
}
variable "admin_key" {
  type      = string
  default   = ""
  sensitive = true
}
