output "api_url" {

  value = aws_api_gateway_stage.dev.invoke_url
}

output "usage_plan_id" {
  value = aws_api_gateway_usage_plan.nova_basic_tier.id
}