output "vectors_table_name" {
  value = aws_dynamodb_table.vectors.name
}

output "chatbot_configs_table_name" {
  value = aws_dynamodb_table.chatbot_configs.name
}

output "chat_sessions_table_name" {
  value = aws_dynamodb_table.chat_sessions.name
}
output "vectors_table_arn" {
  value = aws_dynamodb_table.vectors.arn
}

output "configs_table_arn" {
  value = aws_dynamodb_table.chatbot_configs.arn
}

output "sessions_table_arn" {
  value = aws_dynamodb_table.chat_sessions.arn
}

output "chatbot_configs_table_arn" {
  value       = aws_dynamodb_table.chatbot_configs.arn
  description = "The ARN of the chatbot configurations table"
}

output "chatbot_configs_table_name" {
  value       = aws_dynamodb_table.chatbot_configs.name
  description = "The Name of the chatbot configurations table"
}