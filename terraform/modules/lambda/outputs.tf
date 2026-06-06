output "chat_lambda_arn" {
  value = aws_lambda_function.chat.arn
}

output "crawl_lambda_arn" {
  value = aws_lambda_function.crawl.arn
}

output "ingest_lambda_arn" {
  value = aws_lambda_function.ingest.arn
}