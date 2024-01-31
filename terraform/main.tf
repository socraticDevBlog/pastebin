terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.34.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.4.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.4.1"
    }
  }

  required_version = "1.7.2"
}

provider "aws" {
  profile = "default"
  region  = var.region
}

resource "random_string" "random" {
  length  = 4
  special = false
}

resource "aws_dynamodb_table" "paste" {
  name           = var.dynamodb_table
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 3
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

# #========================================================================
# // lambda setup
# #========================================================================

resource "aws_s3_bucket" "lambda_bucket" {
  bucket_prefix = var.app_name
  force_destroy = true

  tags = {
    App         = "pastebin"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_ownership_controls" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "private_bucket" {
  depends_on = [aws_s3_bucket_ownership_controls.lambda_bucket]
  bucket     = aws_s3_bucket.lambda_bucket.id
  acl        = "private"
}

resource "null_resource" "dependencies_layer" {
  triggers = {
    source_file = "$HOME/.local/share/virtualenvs/pastebin-${var.virtualenv_id}/lib"
    dest_file   = var.compressed_dependencies_layer_filename
  }
  provisioner "local-exec" {
    command = <<EOT
      mkdir python
      cp -r ${self.triggers.source_file} python/
      zip -r ${self.triggers.dest_file} python/
    EOT
  }
}

resource "aws_lambda_layer_version" "dependencies_layer" {
  filename            = var.compressed_dependencies_layer_filename
  layer_name          = "python-layer"
  source_code_hash    = base64sha256(null_resource.dependencies_layer.triggers.dest_file)
  compatible_runtimes = [var.python_runtime]
}

data "archive_file" "lambda_zip" {
  type = "zip"

  source_dir  = "../src"
  output_path = "${path.module}/${var.compressed_app_filename}"
}

resource "aws_s3_object" "this" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = var.compressed_app_filename
  source = data.archive_file.lambda_zip.output_path

  etag = filemd5(data.archive_file.lambda_zip.output_path)
}

//Define lambda function
resource "aws_lambda_function" "apigw_lambda_ddb" {
  function_name = "${var.app_name}-${random_string.random.id}"
  description   = "serverlessland pattern"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.this.key

  runtime = var.python_runtime
  handler = "app.lambda_handler"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  role = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      DDB_TABLE     = var.dynamodb_table,
      AWS_SAM_LOCAL = "",
      DEVENV        = ""
    }
  }
  layers     = [aws_lambda_layer_version.dependencies_layer.arn]
  depends_on = [aws_cloudwatch_log_group.lambda_logs]
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${var.app_name}-${random_string.random.id}"

  retention_in_days = var.log_retention
}

resource "aws_iam_role" "lambda_exec" {
  name = "LambdaDdbPost"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_exec_role" {
  name = "lambda-tf-pattern-ddb-post"

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/${var.dynamodb_table}"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_exec_role.arn
}

# #========================================================================
# // API Gateway section
# #========================================================================

resource "aws_apigatewayv2_api" "http_lambda" {
  name          = "${var.app_name}-${random_string.random.id}"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins     = var.cors_allow_origins
    allow_methods     = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_credentials = false
    allow_headers     = ["accept", "Content-Type", "X-Amz-Date", "Authorization", "x-api-key", "x-amz-security-token", "Auth", "apigw-requestid", "date"]
    max_age           = 300
    expose_headers    = ["accept", "Content-Type", "X-Amz-Date", "Authorization", "x-api-key", "x-amz-security-token", "Auth", "apigw-requestid", "date"]
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.http_lambda.id

  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }

  default_route_settings {
    throttling_burst_limit = 1
    throttling_rate_limit  = 1
  }

  route_settings {
    route_key              = aws_apigatewayv2_route.get.route_key
    throttling_burst_limit = 5
    throttling_rate_limit  = 2
  }

  route_settings {
    route_key              = aws_apigatewayv2_route.post.route_key
    throttling_burst_limit = 2
    throttling_rate_limit  = 1
  }

  depends_on = [aws_cloudwatch_log_group.api_gw]
}

resource "aws_apigatewayv2_integration" "apigw_lambda" {
  api_id = aws_apigatewayv2_api.http_lambda.id

  integration_uri    = aws_lambda_function.apigw_lambda_ddb.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get" {
  api_id = aws_apigatewayv2_api.http_lambda.id

  route_key = "GET /paste"
  target    = "integrations/${aws_apigatewayv2_integration.apigw_lambda.id}"
}

resource "aws_apigatewayv2_route" "post" {
  api_id = aws_apigatewayv2_api.http_lambda.id

  route_key = "POST /paste"
  target    = "integrations/${aws_apigatewayv2_integration.apigw_lambda.id}"
}

resource "aws_apigatewayv2_route" "options" {
  api_id = aws_apigatewayv2_api.http_lambda.id

  route_key = "OPTIONS /paste"
  target    = "integrations/${aws_apigatewayv2_integration.apigw_lambda.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${var.app_name}-${random_string.random.id}"

  retention_in_days = var.log_retention
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.apigw_lambda_ddb.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.http_lambda.execution_arn}/*/*"
}

resource "aws_cloudwatch_metric_alarm" "budget_alarm" {
  alarm_name          = "MonthlyChargeAlarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "EstimatedCharges"
  namespace           = "AWS/Billing"
  period              = 86400 # 1 day in seconds
  statistic           = "Maximum"
  threshold           = 1.0

  dimensions = {
    Currency = "USD"
  }

  alarm_description = "pastebin Alarm for exceeding budget threshold of one dollar USD per month"

  alarm_actions = [aws_sns_topic.budget_notification.arn]
}

resource "aws_sns_topic" "budget_notification" {
  name = "BudgetNotificationTopic"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.budget_notification.arn
  protocol  = "email"
  endpoint  = var.notification_email
}