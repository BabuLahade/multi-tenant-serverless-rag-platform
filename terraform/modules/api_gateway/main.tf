resource "aws_api_gateway_rest_api" "rag_api" {

  name = "nova-rag-api"
}

resource "aws_api_gateway_resource" "chat" {
  rest_api_id = aws_api_gateway_rest_api.rag_api.id
  parent_id   = aws_api_gateway_rest_api.rag_api.root_resource_id

  path_part = "chat"
}

resource "aws_api_gateway_method" "chat_post" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.chat.id

  http_method = "POST"

  authorization = "CUSTOM"

  authorizer_id = aws_api_gateway_authorizer.nova.id
}

resource "aws_api_gateway_integration" "chat" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.chat.id

  http_method = aws_api_gateway_method.chat_post.http_method

  integration_http_method = "POST"

  type = "AWS_PROXY"

  uri = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${var.chat_lambda_arn}/invocations"
}

resource "aws_api_gateway_method" "chat_options" {
  rest_api_id = aws_api_gateway_rest_api.rag_api.id
  resource_id = aws_api_gateway_resource.chat.id
  http_method = "OPTIONS"
  authorization = "NONE"

}

resource "aws_api_gateway_integration" "chat_options" {
  rest_api_id = aws_api_gateway_rest_api.rag_api.id
  resource_id = aws_api_gateway_resource.chat.id
  http_method = aws_api_gateway_method.chat_options.http_method 
  type = "MOCK"
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "chat_options" {
  rest_api_id = aws_api_gateway_rest_api.rag_api.id
  resource_id = aws_api_gateway_resource.chat.id
  http_method = aws_api_gateway_method.chat_options.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}


resource "aws_api_gateway_integration_response" "chat_options" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.chat.id

  http_method = aws_api_gateway_method.chat_options.http_method

  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,POST'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [
    aws_api_gateway_integration.chat_options
  ]
}

data "aws_region" "current" {}

resource "aws_lambda_permission" "chat" {

  statement_id = "AllowApiGatewayChat"

  action = "lambda:InvokeFunction"

  function_name = var.chat_lambda_name

  principal = "apigateway.amazonaws.com"
}

resource "aws_api_gateway_resource" "crawl" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  parent_id = aws_api_gateway_rest_api.rag_api.root_resource_id

  path_part = "crawl"
}

resource "aws_api_gateway_method" "crawl_post" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.crawl.id

  http_method = "POST"

  authorization = "CUSTOM"

  authorizer_id = aws_api_gateway_authorizer.nova.id
}

resource "aws_api_gateway_integration" "crawl" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.crawl.id

  http_method             = aws_api_gateway_method.crawl_post.http_method
  integration_http_method = "POST"

  type = "AWS_PROXY"

  uri = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${var.crawl_lambda_arn}/invocations"
}

resource "aws_api_gateway_method" "crawl_options" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.crawl.id

  http_method = "OPTIONS"

  authorization = "NONE"
}


resource "aws_api_gateway_integration" "crawl_options" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.crawl.id

  http_method = aws_api_gateway_method.crawl_options.http_method

  type = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}


resource "aws_api_gateway_method_response" "crawl_options" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.crawl.id

  http_method = aws_api_gateway_method.crawl_options.http_method

  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}


resource "aws_api_gateway_integration_response" "crawl_options" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  resource_id = aws_api_gateway_resource.crawl.id

  http_method = aws_api_gateway_method.crawl_options.http_method

  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,POST'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [
    aws_api_gateway_integration.crawl_options
  ]
}


resource "aws_lambda_permission" "crawl" {

  statement_id = "AllowApiGatewayCrawl"

  action = "lambda:InvokeFunction"

  function_name = var.crawl_lambda_name

  principal = "apigateway.amazonaws.com"
}

# resource "aws_api_gateway_deployment" "rag" {

#   depends_on = [
#     aws_api_gateway_integration.chat,
#     aws_api_gateway_integration.crawl ,
#     aws_api_gateway_integration.chat_options,
#     aws_api_gateway_integration.crawl_options
#   ]

#   rest_api_id = aws_api_gateway_rest_api.rag_api.id
# }
resource "aws_api_gateway_deployment" "rag" {

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  depends_on = [
    aws_api_gateway_method.chat_post,
    aws_api_gateway_method.chat_options,
    aws_api_gateway_integration.chat,
    aws_api_gateway_integration.chat_options,
    aws_api_gateway_method_response.chat_options,
    aws_api_gateway_integration_response.chat_options,

    aws_api_gateway_method.crawl_post,
    aws_api_gateway_method.crawl_options,
    aws_api_gateway_integration.crawl,
    aws_api_gateway_integration.crawl_options,
    aws_api_gateway_method_response.crawl_options,
    aws_api_gateway_integration_response.crawl_options
  ]

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.chat.path_part,
      aws_api_gateway_method.chat_post.http_method,
      aws_api_gateway_method.chat_post.authorization,
      aws_api_gateway_integration.chat.integration_http_method,
      aws_api_gateway_integration.chat.type,
      aws_api_gateway_integration.chat.uri,

      aws_api_gateway_method.chat_options.http_method,
      aws_api_gateway_method.chat_options.authorization,
      aws_api_gateway_integration.chat_options.type,
      aws_api_gateway_integration.chat_options.request_templates,
      aws_api_gateway_method_response.chat_options.response_parameters,
      aws_api_gateway_integration_response.chat_options.response_parameters,

      aws_api_gateway_resource.crawl.path_part,
      aws_api_gateway_method.crawl_post.http_method,
      aws_api_gateway_method.crawl_post.authorization,
      aws_api_gateway_integration.crawl.integration_http_method,
      aws_api_gateway_integration.crawl.type,
      aws_api_gateway_integration.crawl.uri,

      aws_api_gateway_method.crawl_options.http_method,
      aws_api_gateway_method.crawl_options.authorization,
      aws_api_gateway_integration.crawl_options.type,
      aws_api_gateway_integration.crawl_options.request_templates,
      aws_api_gateway_method_response.crawl_options.response_parameters,
      aws_api_gateway_integration_response.crawl_options.response_parameters,

      aws_api_gateway_authorizer.nova.identity_source,
      aws_api_gateway_authorizer.nova.type
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}
resource "aws_api_gateway_stage" "dev" {

  deployment_id = aws_api_gateway_deployment.rag.id

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  stage_name           = "dev"
  xray_tracing_enabled = true
}


resource "aws_api_gateway_authorizer" "nova" {

  name = "nova-authorizer"

  rest_api_id = aws_api_gateway_rest_api.rag_api.id

  authorizer_uri = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${var.authorizer_lambda_arn}/invocations"

  type = "REQUEST"

  identity_source = "method.request.header.x-api-key"

  authorizer_result_ttl_in_seconds = 300
}

resource "aws_lambda_permission" "authorizer" {

  statement_id = "AllowApiGatewayAuthorizer"

  action = "lambda:InvokeFunction"

  function_name = var.authorizer_lambda_name

  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.rag_api.execution_arn}/*"
}