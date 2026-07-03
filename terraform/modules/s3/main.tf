resource "aws_s3_bucket" "rag" {
  bucket = var.bucket_name
  

  tags ={
    Environment = var.environment
    ManagedBy   = "Terraform"

  }
}

resource "aws_s3_bucket_versioning" "rag" {
  bucket = aws_s3_bucket.rag.id
    versioning_configuration {
        status = "Enabled"
    }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "rag" {

  bucket = aws_s3_bucket.rag.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

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