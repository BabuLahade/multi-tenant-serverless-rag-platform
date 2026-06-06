resource "aws_api_gateway_rest_api" "rag_api" {

  name = "nova-rag-api"
}

resource "aws_api_gateway_resource" "chat" {
  rest_api_id= aws_api_gateway_rest_api.rag_api.id
  parent_id = aws_api_gateway_rest_api.rag_api.root_resource_id

  path_part = "chat"
}

resource "aws_api_gateway_method" "chat_post" {

  rest_api_id =aws_api_gateway_rest_api.rag_api.id

  resource_id =aws_api_gateway_resource.chat.id

  http_method = "POST"

  authorization = "NONE"
}

resource "aws_api_gateway_integration" "chat" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.chat.id

  http_method =aws_api_gateway_method.chat_post.http_method

  integration_http_method = "POST"

  type = "AWS_PROXY"

  uri = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${var.chat_lambda_arn}/invocations"
}
data "aws_region" "current" {}

resource "aws_lambda_permission" "chat" {

  statement_id = "AllowApiGatewayChat"

  action = "lambda:InvokeFunction"

  function_name =var.chat_lambda_name

  principal ="apigateway.amazonaws.com"
}

resource "aws_api_gateway_resource" "crawl" {

  rest_api_id =aws_api_gateway_rest_api.rag_api.id

  parent_id = aws_api_gateway_rest_api.rag_api.root_resource_id

  path_part = "crawl"
}

resource "aws_api_gateway_method" "crawl_post" {

  rest_api_id =aws_api_gateway_rest_api.rag_api.id

  resource_id =aws_api_gateway_resource.crawl.id

  http_method = "POST"

  authorization = "NONE"
}

resource "aws_api_gateway_integration" "crawl" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id =aws_api_gateway_resource.crawl.id

  http_method =aws_api_gateway_method.crawl_post.http_method
  integration_http_method = "POST"

  type = "AWS_PROXY"

  uri ="arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${var.crawl_lambda_arn}/invocations"
}


resource "aws_lambda_permission" "crawl" {

  statement_id = "AllowApiGatewayCrawl"

  action = "lambda:InvokeFunction"

  function_name =var.crawl_lambda_name

  principal ="apigateway.amazonaws.com"
}

resource "aws_api_gateway_deployment" "rag" {

  depends_on = [
    aws_api_gateway_integration.chat,
    aws_api_gateway_integration.crawl
  ]

  rest_api_id =  aws_api_gateway_rest_api.rag_api.id
}

resource "aws_api_gateway_stage" "dev" {

  deployment_id =aws_api_gateway_deployment.rag.id

  rest_api_id =aws_api_gateway_rest_api.rag_api.id

  stage_name = "dev"
}