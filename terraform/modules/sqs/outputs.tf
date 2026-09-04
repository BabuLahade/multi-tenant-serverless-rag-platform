output "ingest_queue_arn" {
  value = aws_sqs_queue.ingest_queue.arn
}

output "ingest_queue_url" {
  value = aws_sqs_queue.ingest_queue.url
}

output "dlq_arn" {
  value = aws_sqs_queue.ingest_dlq.arn
}

output "queue_name" {
  value = aws_sqs_queue.ingest_queue.name
}

output "dlq_name" {
  value = aws_sqs_queue.ingest_dlq.name
}

output "sqs_queue_url" {
  value = aws_sqs_queue.ingest_queue.url
}

output "sqs_queue_arn" {
  value       = aws_sqs_queue.crawl_queue.arn
  description = "The ARN of the crawl SQS queue"
}

output "sqs_queue_url" {
  value       = aws_sqs_queue.crawl_queue.url
  description = "The URL of the crawl SQS queue"
}