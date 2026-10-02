variable "aws_region" {
  description = "AWS Region"
  type        = string
}

variable "project_name" {
  description = "Project Name"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
}

variable "gemini_api_key" {
  type      = string
  sensitive = true
}

variable "tenant_domains" {
  description = "List of all subdomains to be attached to the CloudFront distribution"
  type        = list(string)
  default     = []
}