resource "aws_s3_bucket_notification" "ingest" {

  bucket = aws_s3_bucket.rag.id

  queue {

    queue_arn = var.ingest_queue_arn

    events = [
      "s3:ObjectCreated:*"
    ]

    filter_prefix = ""

    filter_suffix = ".txt"
  }

  depends_on = [
    aws_s3_bucket.rag
  ]
}