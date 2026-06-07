resource "aws_secretsmanager_secret" "gemini" {
    name = "nova/gemini_api_key"
    recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret_version" "gemini" {
    secret_id     = aws_secretsmanager_secret.gemini.id
    secret_string = var.gemini_api_key
}