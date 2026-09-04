output "lambda_role_arn" {

  value = aws_iam_role.lambda_role.arn
}

output "onboard_lambda_role_arn" {

  value = aws_iam_role.onboard_lambda_role.arn
}