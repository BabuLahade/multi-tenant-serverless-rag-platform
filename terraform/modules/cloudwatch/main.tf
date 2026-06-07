resource "aws_cloudwatch_dashboard" "nova" {

  dashboard_name = "nova-rag-dashboard"

  dashboard_body = jsonencode({

    widgets = [

      {
        type = "metric"

        x = 0
        y = 0

        width = 12
        height = 6

        properties = {

          metrics = [
            [
              "AWS/Lambda",
              "Invocations",
              "FunctionName",
              var.chat_lambda_name
            ]
          ]

          view = "timeSeries"

          title = "Chat Lambda Invocations"

          region = "ap-south-1"
        }
      },

      {
        type = "metric"

        x = 12
        y = 0

        width = 12
        height = 6

        properties = {

          metrics = [
            [
              "AWS/SQS",
              "ApproximateNumberOfMessagesVisible",
              "QueueName",
              var.queue_name
            ]
          ]

          view = "timeSeries"

          title = "Queue Depth"

          region = "ap-south-1"
        }
      }
    ]
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

  comparison_operator ="GreaterThanThreshold"

  alarm_description = "Messages found in DLQ"
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

  comparison_operator ="GreaterThanThreshold"
}

resource "aws_cloudwatch_metric_alarm" "queue_age" {

  alarm_name = "nova-queue-age"

  namespace = "AWS/SQS"

  metric_name ="ApproximateAgeOfOldestMessage"

  dimensions = {
    QueueName = var.queue_name
  }

  statistic = "Maximum"

  period = 300

  evaluation_periods = 1

  threshold = 300

  comparison_operator ="GreaterThanThreshold"
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
}