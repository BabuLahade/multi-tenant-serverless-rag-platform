variable "environment" {
  type = string
}

variable "project_name" {
  type = string
}

variable "lambda_role_arn" {
  type = string
}

variable "ingest_queue_arn" {
  type = string
}

# variable "lambda_role_arn" {
#   type = string
# }

# variable "ingest_queue_arn" {
#   type = string
# }

variable "sqs_queue_url" {
  type = string
}

variable "onboard_lambda_role_arn" {
  type = string
}

variable "chatbot_configs_table_name" {
  type = string
}

# variable "sqs_queue_url" {
#   type = string
# }

# variable "usage_plan_id" {
#   type = string
# }