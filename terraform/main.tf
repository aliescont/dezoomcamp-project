terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}

# Bigquery table
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table

resource "google_bigquery_table" "default" {
  dataset_id = var.BQ_DATASET
  table_id   = var.BQ_TABLE

  time_partitioning {
    type = "DAY"
    field = "timestamp_created"
  }

  schema = <<EOF
[
    {"name": "app_id",
    "type": "INTEGER",
    "mode": "NULLABLE"
    }, 
    {"name": "app_name",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "review_id",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "language",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "review",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "timestamp_created",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
    },
    {"name": "timestamp_updated",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
    },
    {"name": "recommended",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
    },
    {"name": "votes_helpful",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "votes_funny",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "weighted_vote_score",
    "type": "FLOAT",
    "mode": "NULLABLE"
    },
    {"name": "comment_count",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "steam_purchase",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
    },
    {"name": "received_for_free",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
    },
    {"name": "written_during_early_access",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
    },
    {"name": "author_steamid",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "author_num_games_owned",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "author_num_reviews",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "author_playtime_forever",
    "type": "FLOAT",
    "mode": "NULLABLE"
    },
    {"name": "author_playtime_last_two_weeks",
    "type": "FLOAT",
    "mode": "NULLABLE"
    },
    {"name": "author_playtime_at_review",
    "type": "FLOAT",
    "mode": "NULLABLE"
    },
    {"name": "author_last_played",
    "type": "FLOAT",
    "mode": "NULLABLE"
    }	
]
EOF

deletion_protection = "false"
}