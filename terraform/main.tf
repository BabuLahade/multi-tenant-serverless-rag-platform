module "raw_content_bucket" {

  source = "./modules/s3"

  bucket_name = "nova-raw-content-169748358276"

  environment = var.environment

  ingest_queue_arn = module.sqs.ingest_queue_arn
  bucket_arn       = module.raw_content_bucket.bucket_arn
  ingest_queue_url = module.sqs.ingest_queue_url

}

module "dynamodb" {

  source = "./modules/dynamodb"

  environment  = var.environment
  project_name = var.project_name
}

module "iam" {

  source = "./modules/IAM"

  project_name       = var.project_name
  environment        = var.environment
  vectors_table_arn  = module.dynamodb.vectors_table_arn
  configs_table_arn  = module.dynamodb.configs_table_arn
  sessions_table_arn = module.dynamodb.sessions_table_arn
  s3_bucket_arn      = module.raw_content_bucket.bucket_arn
  secret_arn         = module.secrets_manager.secret_arn
  ingest_queue_arn   = module.sqs.ingest_queue_arn
  chatbot_configs_table_arn = module.dynamodb.chatbot_configs_table_arn
  sqs_queue_arn = module.sqs.sqs_queue_arn
}


module "lambda" {

  source = "./modules/lambda"

  environment      = var.environment
  project_name     = var.project_name
  lambda_role_arn  = module.iam.lambda_role_arn
  ingest_queue_arn = module.sqs.ingest_queue_arn
  sqs_queue_url = module.sqs.sqs_queue_url
  onboard_lambda_role_arn = module.iam.onboard_lambda_role_arn
  chatbot_configs_table_name = module.dynamodb.chatbot_configs_table_name
  # usage_plan_id = module.api_gateway.usage_plan_id

}

module "api_gateway" {

  source = "./modules/api_gateway"

  chat_lambda_arn = module.lambda.chat_lambda_arn

  chat_lambda_name = module.lambda.chat_lambda_name

  crawl_lambda_arn = module.lambda.crawl_lambda_arn

  crawl_lambda_name = module.lambda.crawl_lambda_name

  authorizer_lambda_arn = module.lambda.authorizer_lambda_arn

  authorizer_lambda_name = module.lambda.authorizer_lambda_name

  onboard_lambda_invoke_arn = module.lambda.onboard_lambda_invoke_arn
  onboard_lambda_name = module.lambda.onboard_lambda_name
  # onboard_lambda_arn = module.lambda.onboard_lambda_arn
}

module "sqs" {

  source = "./modules/sqs"

  environment = var.environment

  project_name = var.project_name
  # s3_bucket_arn = module.raw_content_bucket.bucket_arn
}

module "eventbridge" {

  source = "./modules/eventbridge"

  crawl_lambda_arn  = module.lambda.crawl_lambda_arn
  crawl_lambda_name = module.lambda.crawl_lambda_name
}

module "secrets_manager" {

  source = "./modules/secrets_manager"

  gemini_api_key = var.gemini_api_key
}

module "cloudwatch" {

  source = "./modules/cloudwatch"

  chat_lambda_name = module.lambda.chat_lambda_name

  crawl_lambda_name = module.lambda.crawl_lambda_name

  ingest_lambda_name = module.lambda.ingest_lambda_name

  queue_name = module.sqs.queue_name

  dlq_name = module.sqs.dlq_name
}

module "github_oidc" {

  source = "./modules/github_oidc"

  github_repo = "BabuLahade/multi-tenant-serverless-rag-platform"
}

module "cdn" {
  source = "./modules/cdn"

  providers = {
    aws.us_east_1 = aws.us_east_1
  }

  root_domain    = "babu-lahade.online"
  domain_aliases = ["cdn.babu-lahade.online"]
}