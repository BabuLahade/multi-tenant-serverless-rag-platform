output "chat_lambda_arn" {
  value = aws_lambda_function.chat.arn
}

output "crawl_lambda_arn" {
  value = aws_lambda_function.crawl.arn
}

output "ingest_lambda_arn" {
  value = aws_lambda_function.ingest.arn
}

output "chat_lambda_name" {
  value = aws_lambda_function.chat.function_name
}

output "crawl_lambda_name" {
  value = aws_lambda_function.crawl.function_name
}

output "ingest_lambda_name" {
  value = aws_lambda_function.ingest.function_name
}

output "authorizer_lambda_arn" {
  value = aws_lambda_function.authorizer.arn
}

output "authorizer_lambda_name" {
  value = aws_lambda_function.authorizer.function_name
}

output "onboard_lambda_arn" {
  value = aws_lambda_function.nova_onboard.arn
}
output "onboard_lambda_invoke_arn" {
  value = aws_lambda_function.nova_onboard.invoke_arn
}

output "onboard_lambda_name" {
  value = aws_lambda_function.nova_onboard.function_name
}