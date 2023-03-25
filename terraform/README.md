# Terraform

In this project Terraform was used to create infraestructuren on GCP, such as Bucket(Data Lake) and Bigquery dataset(DWH)


## Previous steps

### Google Cloud setup

- Create a new project in Google Cloud
- Go to IAM and create a service account
- Create a service account key with BigQuery Admin and Storage Admin roles
- Install Google Cloud SDK

### Install Terraform

- Install Terraform following the instructions for your corresponding OS

## Terraform files

.terraform-version: this file contains the version installed

main.tf: this file contains resources to be created by Terraform. 
First, we set the version and backend -> "local" means that terraform.tfstate will be create locally. If you want to have it online, you can change for "gcs" 
Then, we set provider and resources to create a Bucket and a dataset in BigQuery for the project and region declared in variables.

variables.tf: this file contains the variables declaration used 

## Terraform commands 

To create resources in GCP using Terraform, after changing accordingly variables in Terraform files, you need to execute the following commands

```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan 

# Create new infra
terraform apply 
```


## Resources

Week 1 of [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp)