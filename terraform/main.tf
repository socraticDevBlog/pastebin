terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.25.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.7.2"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.7.1"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.6.1"
    }
  }

  required_version = "1.14.1"
}

provider "aws" {
  region = var.region
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
  ttl {
    attribute_name = "ttl"
    enabled        = true
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

data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = "../.venv/lib"
  output_path = "${path.module}/${var.zipped_files["layer"]}"
}

resource "aws_lambda_layer_version" "dependencies_layer" {
  filename            = var.zipped_files["layer"]
  layer_name          = "python-layer"
  source_code_hash    = data.archive_file.layer_zip.output_sha
  compatible_runtimes = [var.python_runtime]
}

data "archive_file" "lambda_zip" {
  type = "zip"

  source_dir  = "../src"
  output_path = "${path.module}/${var.zipped_files["app"]}"
}

resource "aws_s3_object" "this" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = var.zipped_files["app"]
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

  source_code_hash = filebase64sha256(data.archive_file.lambda_zip.output_path)

  role = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      DDB_TABLE     = var.dynamodb_table,
      PASTE_TTL     = 259200, # a paste self-deletes 3 days after insert
      AWS_SAM_LOCAL = "",
      DEVENV        = "",
      BASE_URL      = var.api_base_url
    }
  }
  layers = [aws_lambda_layer_version.dependencies_layer.arn]
  lifecycle {
    ignore_changes = [
      layers,
    ]
  }
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
                "dynamodb:UpdateItem",
                "dynamodb:Scan"
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

  dynamic "route_settings" {
    for_each = aws_apigatewayv2_route.read

    content {
      route_key              = route_settings.value.route_key
      throttling_burst_limit = 1
      throttling_rate_limit  = 1
    }
  }

  dynamic "route_settings" {
    for_each = aws_apigatewayv2_route.write

    content {
      route_key              = route_settings.value.route_key
      throttling_burst_limit = 1
      throttling_rate_limit  = 1
    }
  }
  depends_on = [aws_cloudwatch_log_group.api_gw]
}

resource "aws_apigatewayv2_integration" "apigw_lambda" {
  api_id = aws_apigatewayv2_api.http_lambda.id

  integration_uri    = aws_lambda_function.apigw_lambda_ddb.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "read" {
  for_each = var.routes_read

  route_key = each.key
  api_id    = aws_apigatewayv2_api.http_lambda.id
  target    = "integrations/${aws_apigatewayv2_integration.apigw_lambda.id}"
}

resource "aws_apigatewayv2_route" "write" {
  for_each = var.routes_write

  route_key = each.key
  api_id    = aws_apigatewayv2_api.http_lambda.id
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

locals {
  email_alarm_topics = {
    budget_notification       = aws_sns_topic.budget_notification.arn
    api_requests_notification = aws_sns_topic.api_requests_notification.arn
  }
}

moved {
  from = aws_sns_topic_subscription.email_subscription
  to   = aws_sns_topic_subscription.email_alerts["budget_notification"]
}

resource "aws_sns_topic_subscription" "email_alerts" {
  for_each  = local.email_alarm_topics
  topic_arn = each.value
  protocol  = "email"
  endpoint  = var.notification_email
}

resource "aws_cloudwatch_metric_alarm" "api_requests_alarm" {
  alarm_name          = "APIGatewayRequestAlarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Count"
  namespace           = "AWS/ApiGateway"
  period              = 1200 # 20 minutes (adjust as needed)
  statistic           = "Sum"
  threshold           = 1000 # Trigger alarm when requests exceed 1000

  dimensions = {
    ApiId = aws_apigatewayv2_api.http_lambda.id
  }

  alarm_description = "Alarm for API Gateway requests exceeding 10,000 in the evaluation period."

  alarm_actions = [aws_sns_topic.api_requests_notification.arn]
}

resource "aws_sns_topic" "api_requests_notification" {
  name = "APIRequestsNotificationTopic"
}
