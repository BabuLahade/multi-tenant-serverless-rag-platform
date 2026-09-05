resource "aws_lambda_layer_version" "python" {

  layer_name = "nova-python-layer"

  filename = "${path.root}/../lambda/packages/python-layer.zip"

  source_code_hash = filebase64sha256(
    "${path.root}/../lambda/packages/python-layer.zip"
  )

  compatible_runtimes = [
    "python3.12"
  ]

  description = "Shared Python dependencies for Nova RAG"
}

resource "aws_lambda_function" "chat" {
  function_name = "nova-chat"
  role          = var.lambda_role_arn
  handler       = "handler.handler"
  runtime       = "python3.12"
  layers = [
    aws_lambda_layer_version.python.arn
  ]
  filename = "${path.root}/../lambda/packages/nova-chat.zip"

  source_code_hash = filebase64sha256(
    "${path.root}/../lambda/packages/nova-chat.zip"
  )
  tracing_config {
    mode = "Active"
  }


  timeout = 30

  memory_size = 512
}

resource "aws_lambda_function" "crawl" {

  function_name = "nova-crawl"

  role = var.lambda_role_arn

  runtime = "python3.12"

  handler = "handler.handler"

  layers = [
    aws_lambda_layer_version.python.arn
  ]

  filename = "${path.root}/../lambda/packages/nova-crawl.zip"

  source_code_hash = filebase64sha256(
    "${path.root}/../lambda/packages/nova-crawl.zip"
  )
  tracing_config {
    mode = "Active"
  }
  environment {
    variables = {
      SQS_QUEUE_URL = var.sqs_queue_url
    }
  }
  timeout = 60

  memory_size = 512
}

resource "aws_lambda_function" "ingest" {

  function_name = "nova-ingest"

  role = var.lambda_role_arn

  runtime = "python3.12"

  handler = "handler.handler"
  layers = [
    aws_lambda_layer_version.python.arn
  ]

  filename = "${path.root}/../lambda/packages/nova-ingest.zip"

  source_code_hash = filebase64sha256(
    "${path.root}/../lambda/packages/nova-ingest.zip"
  )
  tracing_config {
    mode = "Active"
  }
  timeout = 120

  memory_size = 1024
}

resource "aws_lambda_event_source_mapping" "ingest" {

  event_source_arn = var.ingest_queue_arn

  function_name = aws_lambda_function.ingest.arn

  batch_size = 5

  enabled = true
}


resource "aws_lambda_function" "authorizer" {

  function_name = "nova-authorizer"

  role = var.lambda_role_arn

  runtime = "python3.12"

  handler = "handler.handler"

  filename = "${path.root}/../lambda/packages/nova-authorizer.zip"

  source_code_hash = filebase64sha256(
    "${path.root}/../lambda/packages/nova-authorizer.zip"
  )

  timeout = 5

  memory_size = 128

  tracing_config {
    mode = "Active"
  }
}


resource "aws_lambda_function" "nova_onboard" {
  filename      = "../lambda/packages/nova-onboard.zip" # Make sure this matches your zip path
  function_name = "nova-onboard"
  role          = var.onboard_lambda_role_arn
  handler       = "handler.handler"
  runtime       = "python3.12"
  
  environment {
    variables = {
      CONFIGS_TABLE = var.chatbot_configs_table_name
      # Replace 'aws_sqs_queue.crawl_queue.url' with your actual SQS URL reference
      SQS_QUEUE_URL = var.sqs_queue_url
      USAGE_PLAN_ID = var.usage_plan_id
      WIDGET_URL    = "https://babulahade.github.io/multi-tenant-serverless-rag-platform/frontend/widget.js"
    }
  }
}