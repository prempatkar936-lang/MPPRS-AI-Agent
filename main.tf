# Google Cloud Run deployment for MPPRS AI Agent

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Cloud Run Service
resource "google_cloud_run_service" "mpprs_ai_agent" {
  name     = "mpprs-ai-agent"
  location = var.gcp_region

  template {
    spec {
      containers {
        image = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/cloud-run-source-deploy/mpprs-ai-agent:latest"
        
        env {
          name  = "OPENAI_API_KEY"
          value = var.openai_api_key
        }
        env {
          name  = "DATABASE_HOST"
          value = google_sql_database_instance.mpprs_db.private_ip_address
        }
        env {
          name  = "DATABASE_USER"
          value = google_sql_user.mpprs_user.name
        }
        env {
          name  = "DATABASE_PASSWORD"
          value = google_sql_user.mpprs_user.password
        }
        env {
          name  = "DATABASE_NAME"
          value = google_sql_database.mpprs.name
        }
        env {
          name  = "WHATSAPP_API_TOKEN"
          value = var.whatsapp_api_token
        }
        env {
          name  = "INSTAGRAM_ACCESS_TOKEN"
          value = var.instagram_access_token
        }
        env {
          name  = "FACEBOOK_PAGE_ACCESS_TOKEN"
          value = var.facebook_page_access_token
        }
        env {
          name  = "ENVIRONMENT"
          value = "production"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_sql_database_instance.mpprs_db]
}

# Cloud SQL Instance
resource "google_sql_database_instance" "mpprs_db" {
  name             = "mpprs-db-instance"
  database_version = "POSTGRES_15"
  region           = var.gcp_region

  settings {
    tier            = "db-f1-micro"
    availability_type = "REGIONAL"
    
    database_flags {
      name  = "cloudsql_iam_authentication"
      value = "on"
    }
  }

  deletion_protection = true
}

# Cloud SQL Database
resource "google_sql_database" "mpprs" {
  name     = "MPPRS"
  instance = google_sql_database_instance.mpprs_db.name
}

# Cloud SQL User
resource "google_sql_user" "mpprs_user" {
  name     = "mpprs_user"
  instance = google_sql_database_instance.mpprs_db.name
  password = var.database_password
}

# Cloud Run IAM Binding
resource "google_cloud_run_service_iam_member" "noauth" {
  service  = google_cloud_run_service.mpprs_ai_agent.name
  location = google_cloud_run_service.mpprs_ai_agent.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "cloud_run_url" {
  value = google_cloud_run_service.mpprs_ai_agent.status[0].url
}
