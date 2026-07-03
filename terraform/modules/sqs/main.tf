resource "aws_sqs_queue" "ingest_dlq" {
    name = "nova-ingest_queue"
    message_retention_seconds = 1209600 # 14 days 
}

resource "aws_sqs_queue" "ingest_queue" {
    name = "nova-ingest-queue"

    visibility_timeout_seconds = 300

    redrive_policy = jsonencode({
        deadLetterTargetArn = aws_sqs_queue.ingest_dlq.arn
        maxReceiveCount     = 3
    })
}

resource "aws_sqs_queue_policy" "allow_s3" {

  queue_url = aws_sqs_queue.ingest_queue.id

  policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {

        Effect = "Allow"

        Principal = {
          Service = "s3.amazonaws.com"
        }

        Action = "sqs:SendMessage"

        Resource = aws_sqs_queue.ingest_queue.arn

      }

    ]

  })
}