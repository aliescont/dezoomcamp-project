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

resource "google_bigquery_dataset" "dbt_prod_dataset" {
  dataset_id = var.BQ_DBT_PROD_DATASET
  project    = var.project
  location   = var.region
}

resource "google_bigquery_dataset" "dbt_dev_dataset" {
  dataset_id = var.BQ_DBT_DEV_DATASET
  project    = var.project
  location   = var.region
}

# Bigquery table
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table

resource "google_bigquery_table" "default" {
  dataset_id = var.BQ_DATASET
  table_id   = var.BQ_TABLE

  time_partitioning {
    type = "MONTH"
    field = "timestamp_created"
  }

  schema = <<EOF
[
    {"name": "steamid",
    "type": "INTEGER",
    "mode": "NULLABLE"
    }, 
    {"name": "appid",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "voted_up",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
    },
    {"name": "votes_up",
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
    {"name": "playtime_forever",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "playtime_at_review",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "num_games_owned",
    "type": "INTEGER",
    "mode": "NULLABLE"
    },
    {"name": "num_reviews",
    "type": "INTEGER",
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
    }
]
EOF

deletion_protection = "false"
depends_on = [google_bigquery_dataset.dataset]
}


resource "google_bigquery_table" "default_dim" {
  dataset_id = var.BQ_DATASET
  table_id   = var.BQ_DIM_TABLE

  schema = <<EOF
[
    {"name": "appid",
    "type": "INTEGER",
    "mode": "NULLABLE"
    }, 
    {"name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "short_description",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "developer",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "publisher",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "genre",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "tags",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "categories",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "languages",
    "type": "STRING",
    "mode": "NULLABLE"
    },
    {"name": "release_date",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
    }
]
EOF

deletion_protection = "false"
depends_on = [google_bigquery_dataset.dataset]
}