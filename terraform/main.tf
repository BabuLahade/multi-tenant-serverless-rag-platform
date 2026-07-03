module "raw_content_bucket" {

  source = "./modules/s3"

  bucket_name = "nova-raw-content"

  environment = var.environment

  ingest_queue_arn = module.sqs.ingest_queue_arn
  bucket_arn = module.sqs.ingest_queue_arn
  ingest_queue_url = module.sqs.ingest_queue_url
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
  secret_arn = module.secrets_manager.secret_arn
  ingest_queue_arn = module.sqs.ingest_queue_arn
}


module "lambda" {

  source = "./modules/lambda"

  environment = var.environment
  project_name = var.project_name
  lambda_role_arn = module.iam.lambda_role_arn
  ingest_queue_arn = module.sqs.ingest_queue_arn
  
}

module "api_gateway" {

  source = "./modules/api_gateway"

  chat_lambda_arn =module.lambda.chat_lambda_arn

  chat_lambda_name = module.lambda.chat_lambda_name

  crawl_lambda_arn =module.lambda.crawl_lambda_arn

  crawl_lambda_name =module.lambda.crawl_lambda_name
}

module "sqs" {

  source = "./modules/sqs"

  environment = var.environment

  project_name = var.project_name
}

module "eventbridge" {

  source = "./modules/eventbridge"

  crawl_lambda_arn =module.lambda.crawl_lambda_arn
  crawl_lambda_name = module.lambda.crawl_lambda_name
}

module "secrets_manager" {

  source = "./modules/secrets_manager"

  gemini_api_key = var.gemini_api_key
}

module "cloudwatch" {

  source = "./modules/cloudwatch"

  chat_lambda_name = module.lambda.chat_lambda_name

  crawl_lambda_name =module.lambda.crawl_lambda_name

  ingest_lambda_name =module.lambda.ingest_lambda_name

  queue_name =module.sqs.queue_name

  dlq_name =module.sqs.dlq_name
}

module "github_oidc" {

  source = "./modules/github_oidc"

  github_repo ="BabuLahade/multi-tenant-serverless-rag-platform"
}

