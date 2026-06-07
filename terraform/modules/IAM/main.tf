data "aws_iam_policy_document" "lambda_assume_role" {

  statement {

    effect = "Allow"

    actions = [
      "sts:AssumeRole"
    ]

    principals {

      type = "Service"

      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "lambda_role" {

  name = "nova-lambda-role"

  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "logs" {

  role = aws_iam_role.lambda_role.name

  policy_arn ="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "xray" {

  role = aws_iam_role.lambda_role.name

  policy_arn =  "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}


resource "aws_iam_policy" "lambda_data_access" {

  name = "nova-lambda-data-access"

  policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {
        Effect = "Allow"

        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:UpdateItem"
        ]

        Resource = [
          var.vectors_table_arn,
          var.configs_table_arn,
          var.sessions_table_arn
        ]
      },

      {
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]

        Resource = [
          var.s3_bucket_arn,
          "${var.s3_bucket_arn}/*"
        ]
      },

      {
        Effect = "Allow"

        Action = [
          "secretsmanager:GetSecretValue"
        ]

        Resource = "*"
      } ,
      {
        Effect = "Allow"

        Action = [
            "sqs:SendMessage",
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes"
        ]

        Resource = "*"
      },
      {
        Effect = "Allow"

        Action = [
        "secretsmanager:GetSecretValue"
         ]

         Resource = [
             var.secret_arn
            ]
        }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "data_access" {

  role = aws_iam_role.lambda_role.name

  policy_arn = aws_iam_policy.lambda_data_access.arn
}