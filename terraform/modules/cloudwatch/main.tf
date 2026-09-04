resource "aws_sns_topic" "nova_alerts" {
  name = "nova-rag-alerts"
}


resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.nova_alerts.arn
  protocol  = "email"
  endpoint  = "babulahade@gmail.com"
}


resource "aws_cloudwatch_dashboard" "nova" {

  dashboard_name = "nova-rag-dashboard"

  dashboard_body = jsonencode({
    widgets = [
  {
    type       = "metric"
    x = 0 
    y = 0
    width = 12
     height = 6
    properties = {
      metrics = [["AWS/Lambda", "Invocations", "FunctionName", var.chat_lambda_name]]
      view    = "timeSeries"
      title   = "Chat Lambda Invocations"
      region  = "ap-south-1"
    }
  },
  {
    type       = "metric"
    x = 12
     y = 0
    width = 12
     height = 6
    properties = {
      metrics = [["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", var.queue_name]]
      view    = "timeSeries"
      title   = "Queue Depth"
      region  = "ap-south-1"
    }
  },
  {
    type       = "metric"
    x = 0
      y = 6
    width = 12
     height = 6
    properties = {
      metrics = [["AWS/Lambda", "Errors", "FunctionName", var.chat_lambda_name]]
      view    = "timeSeries"
      title   = "Chat Lambda Errors"
      region  = "ap-south-1"
    }
  },
  {
    type       = "metric"
    x = 12
     y = 6
    width = 12
    height = 6
    properties = {
      metrics = [["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", var.dlq_name]]
      view    = "timeSeries"
      title   = "DLQ Depth"
      region  = "ap-south-1"
    }
  },
  {
    type       = "metric"
    x = 0
      y = 12
    width = 24
     height = 6
    properties = {
      metrics = [["AWS/Lambda", "Duration", "FunctionName", var.chat_lambda_name, { stat = "p99" }]]
      view    = "timeSeries"
      title   = "Chat Lambda p99 Latency (ms)"
      region  = "ap-south-1"
    }
  }
]

    # widgets = [

    #   {
    #     type = "metric"

    #     x = 0
    #     y = 0

    #     width  = 12
    #     height = 6

    #     properties = {

    #       metrics = [
    #         [
    #           "AWS/Lambda",
    #           "Invocations",
    #           "FunctionName",
    #           var.chat_lambda_name
    #         ]
    #       ]

    #       view = "timeSeries"

    #       title = "Chat Lambda Invocations"

    #       region = "ap-south-1"
    #     }
    #   },

    #   {
    #     type = "metric"

    #     x = 12
    #     y = 0

    #     width  = 12
    #     height = 6

    #     properties = {

    #       metrics = [
    #         [
    #           "AWS/SQS",
    #           "ApproximateNumberOfMessagesVisible",
    #           "QueueName",
    #           var.queue_name
    #         ]
    #       ]

    #       view = "timeSeries"

    #       title = "Queue Depth"

    #       region = "ap-south-1"
    #     }
    #   }
    # ]
  })
}


resource "aws_cloudwatch_metric_alarm" "dlq_depth" {

  alarm_name = "nova-dlq-depth"

  namespace = "AWS/SQS"

  metric_name = "ApproximateNumberOfMessagesVisible"

  dimensions = {
    QueueName = var.dlq_name
  }

  statistic = "Maximum"

  period = 300

  evaluation_periods = 1

  threshold = 0

  comparison_operator = "GreaterThanThreshold"

  alarm_description = "Messages found in DLQ"
  alarm_actions       = [aws_sns_topic.nova_alerts.arn]
  ok_actions          = [aws_sns_topic.nova_alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "chat_errors" {

  alarm_name = "nova-chat-errors"

  namespace = "AWS/Lambda"

  metric_name = "Errors"

  dimensions = {
    FunctionName = var.chat_lambda_name
  }

  statistic = "Sum"

  period = 300

  evaluation_periods = 1

  threshold = 5

  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.nova_alerts.arn]
  ok_actions          = [aws_sns_topic.nova_alerts.arn]
}
resource "aws_cloudwatch_metric_alarm" "ingest_errors" {
  alarm_name          = "nova-ingest-errors"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  dimensions = {
    FunctionName = var.ingest_lambda_name
  }
  statistic           = "Sum"
  period              = 60
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"
  alarm_description   = "Triggered when background crawler/ingest Lambda errors out."
  alarm_actions       = [aws_sns_topic.nova_alerts.arn]
  ok_actions          = [aws_sns_topic.nova_alerts.arn]
}
resource "aws_cloudwatch_metric_alarm" "queue_age" {

  alarm_name = "nova-queue-age"

  namespace = "AWS/SQS"

  metric_name = "ApproximateAgeOfOldestMessage"

  dimensions = {
    QueueName = var.queue_name
  }

  statistic = "Maximum"

  period = 300

  evaluation_periods = 1

  threshold = 300

  comparison_operator = "GreaterThanThreshold"

  alarm_actions       = [aws_sns_topic.nova_alerts.arn]
  ok_actions          = [aws_sns_topic.nova_alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "chat_duration" {

  alarm_name = "nova-chat-duration"

  namespace = "AWS/Lambda"

  metric_name = "Duration"

  dimensions = {
    FunctionName = var.chat_lambda_name
  }

  extended_statistic = "p99"

  period = 300

  evaluation_periods = 1

  threshold = 8000

  comparison_operator = "GreaterThanThreshold"

  alarm_actions       = [aws_sns_topic.nova_alerts.arn]
  ok_actions          = [aws_sns_topic.nova_alerts.arn]
}