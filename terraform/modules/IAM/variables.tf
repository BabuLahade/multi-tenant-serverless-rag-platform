variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "vectors_table_arn" {
  type = string
}

variable "configs_table_arn" {
  type = string
}

variable "sessions_table_arn" {
  type = string
}

variable "s3_bucket_arn" {
  type = string
}

variable "secret_arn" {
  type = string
}
variable "ingest_queue_arn" {
  type = string
}

variable "chatbot_configs_table_arn" {
  description = "ARN of the chatbot configs DynamoDB table"
  type        = string
}

variable "sqs_queue_arn" {
  description = "ARN of the SQS crawl queue"
  type        = string
}