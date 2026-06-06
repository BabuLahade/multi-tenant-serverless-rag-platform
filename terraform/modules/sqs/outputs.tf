output "queue_arn" {
  value = aws_sqs_queue.ingest_queue.arn
}

output "queue_url" {
  value = aws_sqs_queue.ingest_queue.url
}

output "dlq_arn" {
  value = aws_sqs_queue.ingest_dlq.arn
}