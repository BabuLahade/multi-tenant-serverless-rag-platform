terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      configuration_aliases = [aws.us_east_1]
    }
  }
}

variable "root_domain" {
  type        = string
  default     = "babu-lahade.online"
  description = "Base domain name"
}

variable "domain_aliases" {
  type        = list(string)
  default     = ["cdn.babu-lahade.online"]
  description = "Subdomains pointing to CloudFront"
}

# 1. Request Wildcard ACM Certificate in us-east-1
resource "aws_acm_certificate" "wildcard" {
  provider                  = aws.us_east_1
  domain_name               = var.root_domain
  subject_alternative_names = ["*.${var.root_domain}"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# 2. Wait for DNS Validation to Complete
# Terraform will pause until you add the CNAME to Hostinger and AWS marks it ISSUED
resource "aws_acm_certificate_validation" "cert_validation" {
  provider        = aws.us_east_1
  certificate_arn = aws_acm_certificate.wildcard.arn
}

# 3. Private S3 Bucket for Static Assets
resource "aws_s3_bucket" "frontend" {
  bucket_prefix = "nova-frontend-assets-"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket                  = aws_s3_bucket.frontend.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 4. CloudFront Origin Access Control (OAC)
resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "nova-frontend-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# 5. CloudFront Distribution
resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "onboard.html"
  aliases             = var.domain_aliases

  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "S3Origin"
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3Origin"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
      headers = ["Origin", "Access-Control-Request-Headers", "Access-Control-Request-Method"]
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.cert_validation.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  depends_on = [aws_acm_certificate_validation.cert_validation]
}

# 6. S3 Bucket Policy (Restricts read access strictly to CloudFront OAC)
resource "aws_s3_bucket_policy" "frontend_cdn_policy" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFrontServicePrincipalReadOnly"
        Effect    = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.frontend.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.cdn.arn
          }
        }
      }
    ]
  })
}

# Outputs for DNS configuration
output "acm_validation_records" {
  description = "CNAME records required by your DNS provider (Hostinger) to validate the certificate"
  value = [
    for dvo in aws_acm_certificate.wildcard.domain_validation_options : {
      name   = dvo.resource_record_name
      type   = dvo.resource_record_type
      record = dvo.resource_record_value
    }
  ]
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.cdn.id
}

output "cloudfront_domain" {
  value = aws_cloudfront_distribution.cdn.domain_name
}

output "frontend_bucket_name" {
  value = aws_s3_bucket.frontend.id
}