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