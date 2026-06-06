resource "aws_sqs_queue" "ingest_queue" {
    name = "nova-ingest_queue"
    message_retention_seconds = 1209600 # 14 days)
}

resource "aws_sqs_queue" "ingest_queue" {
    name = "nova-ingest-queue"

    visibility_timeout_seconds = 300

    redrive_allow_policy = jsonencode({
        deadLetterTargetArn = aws_sqs_queue.dead_letter_queue.arn
        maxReceiveCount = 3
    })
}