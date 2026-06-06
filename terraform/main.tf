module "raw_content_bucket" {

  source = "./modules/s3"

  bucket_name = "nova-raw-content"

  environment = var.environment
}

module "dynamodb" {

  source = "./modules/dynamodb"

  environment = var.environment
  project_name = var.project_name
}