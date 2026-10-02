variable "domain_aliases" {
  description = "List of CNAMEs for the CloudFront distribution"
  type        = list(string)
}