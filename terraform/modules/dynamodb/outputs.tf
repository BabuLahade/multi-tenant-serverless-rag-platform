output "vectors_table_name" {
    value = aws_dynamodb_table.vectors.name
}

output "chatbot_configs_table_name" {
    value = aws_dynamodb_table.chatbot_configs.name
}

output "chat_sessions_table_name" {
    value = aws_dynamodb_table.chat_sessions.name
}