resource "aws_lambda_function" "chat" {
    function_name = "nova-chat"
    role = var.lambda_role_arn
    handler = "handler.handler"
    runtime = "python3.12"

    filename = "${path.root}/../lambda/packages/nova-chat.zip"

    source_code_hash = filebase64sha256(
      "${path.root}/../lambda/packages/nova-chat.zip"
    )

  timeout = 30

  memory_size = 51
}

resource "aws_lambda_function" "crawl" {

  function_name = "nova-crawl"

  role = var.lambda_role_arn

  runtime = "python3.12"

  handler = "handler.handler"

  filename ="${path.root}/../lambda/packages/nova-crawl.zip"

  source_code_hash = filebase64sha256(
      "${path.root}/../lambda/packages/nova-crawl.zip"
    )

  timeout = 60

  memory_size = 512
}

resource "aws_lambda_function" "ingest" {

  function_name = "nova-ingest"

  role = var.lambda_role_arn

  runtime = "python3.12"

  handler = "handler.handler"

  filename ="${path.root}/../lambda/packages/nova-ingest.zip"

  source_code_hash =filebase64sha256(
      "${path.root}/../lambda/packages/nova-ingest.zip"
    )

  timeout = 120

  memory_size = 1024
}