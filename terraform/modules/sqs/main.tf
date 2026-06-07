resource "aws_sqs_queue" "ingest_dlq" {
    name = "nova-ingest_queue"
    message_retention_seconds = 1209600 # 14 days)
}

resource "aws_sqs_queue" "ingest_queue" {
    name = "nova-ingest-queue"

    visibility_timeout_seconds = 300

    redrive_allow_policy = jsonencode({
        deadLetterTargetArn = aws_sqs_queue.ingest_dlq.arn
        maxReceiveCount = 3
    })
}