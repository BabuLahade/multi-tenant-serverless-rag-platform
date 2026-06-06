resource "aws_dynamodb_table" "vectors" {
    name = "nova-vectors"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "client_id"
    range_key = "chunk_id"

    attribute {
      name = "client_id"
      type = "S"
    }
    attribute {
      name = "chunk_id"
      type = "S"
    }

    point_in_time_recovery {
      enabled = true 
    }

    tags = {
        Environment = var.environment
        Project     = var.project_name
    }
}

resource "aws_dynamodb_table" "chatbot_configs" {
    name = "nova-chatbot-configs"
    billing_mode = "PAY_PER_REQUEST"

    hash_key = "client_id"
    attribute {
      name = "client_id"
      type = "S"

    }
    point_in_time_recovery {
      enabled = true 
    }
}

resource "aws_dynamodb_table" "chat_sessions" {

  name         = "nova-chat-sessions"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "session_id"

  attribute {
    name = "session_id"
    type = "S"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }

  point_in_time_recovery {
    enabled = true
  }
}