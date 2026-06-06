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

module "iam" {

  source = "./modules/IAM"

  project_name = var.project_name

  environment = var.environment

  vectors_table_arn = module.dynamodb.vectors_table_arn

  configs_table_arn =module.dynamodb.configs_table_arn

  sessions_table_arn = module.dynamodb.sessions_table_arn

  s3_bucket_arn =module.raw_content_bucket.bucket_arn
}