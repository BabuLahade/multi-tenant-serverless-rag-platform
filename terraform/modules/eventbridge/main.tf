resource "aws_cloudwatch_event_rule" "weekly_crawl" {
    name = "nova-weekly-crawl"

    description = "Triggers the crawl lambda every week"

    schedule_expression = "rate(7 days)"
}

resource "aws_cloudwatch_event_target" "crawl_target" {
  rule = aws_cloudwatch_event_rule.weekly_crawl.name
  arn = var.crawl_lambda_arn
}

resource "aws_lambda_permission" "eventbridge" {
    statement_id = "AllowEventBridge"
    action = "lambda:InvokeFunction"
    function_name = var.crawl_lambda_name
    principal = "events.amazonaws.com"

    source_arn = aws_cloudwatch_event_rule.weekly_crawl.arn
}