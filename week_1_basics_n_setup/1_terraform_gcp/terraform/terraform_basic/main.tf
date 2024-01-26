terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = "taxi-rides-ny-410014"
  region  = "europe-west1"
}

resource "google_storage_bucket" "tera-bucket" {
  name          = "taxi-rides-ny-410014-terra-bucket"
  location      = "europe-west1"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}