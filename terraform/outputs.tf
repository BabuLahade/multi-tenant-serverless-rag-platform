output "project_name" {
  value = var.project_name
}

output "environment" {
  value = var.environment
}

output "aws_region" {
  value = var.aws_region
}

output "acm_dns_validation_records" {
  value       = module.cdn.acm_validation_records
  description = "Paste these CNAME values into Hostinger DNS"
}

output "cdn_domain" {
  value = module.cdn.cloudfront_domain
}

output "assets_bucket" {
  value = module.cdn.frontend_bucket_name
}

output "cdn_distribution_id" {
  value = module.cdn.cloudfront_distribution_id
}