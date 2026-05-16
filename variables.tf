variable "gcp_project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "gcp_region" {
  description = "Google Cloud Region"
  type        = string
  default     = "us-central1"
}

variable "openai_api_key" {
  description = "OpenAI API Key"
  type        = string
  sensitive   = true
}

variable "whatsapp_api_token" {
  description = "WhatsApp Business API Token"
  type        = string
  sensitive   = true
}

variable "instagram_access_token" {
  description = "Instagram Access Token"
  type        = string
  sensitive   = true
}

variable "facebook_page_access_token" {
  description = "Facebook Page Access Token"
  type        = string
  sensitive   = true
}

variable "database_password" {
  description = "Cloud SQL Database Password"
  type        = string
  sensitive   = true
}
