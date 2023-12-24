terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.31.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.4.1"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.4.1"
    }
  }

  required_version = "1.6.6"
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

data "local_file" "dependencies_layer" {
  filename = null_resource.dependencies_layer.triggers.dest_file
}

resource "aws_lambda_layer_version" "dependencies_layer" {
  depends_on          = [null_resource.dependencies_layer]
  filename            = var.compressed_dependencies_layer_filename
  layer_name          = "python-layer"
  source_code_hash    = data.local_file.dependencies_layer.content_base64sha256
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
      AWS_SAM_LOCAL = "false",
      DEVENV        = "false"
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

# resource "aws_apigatewayv2_api" "http_lambda" {
#   name          = "${var.app_name}-${random_string.random.id}"
#   protocol_type = "HTTP"
# }

# resource "aws_apigatewayv2_stage" "default" {
#   api_id = aws_apigatewayv2_api.http_lambda.id

#   name        = "$default"
#   auto_deploy = true

#   access_log_settings {
#     destination_arn = aws_cloudwatch_log_group.api_gw.arn

#     format = jsonencode({
#       requestId               = "$context.requestId"
#       sourceIp                = "$context.identity.sourceIp"
#       requestTime             = "$context.requestTime"
#       protocol                = "$context.protocol"
#       httpMethod              = "$context.httpMethod"
#       resourcePath            = "$context.resourcePath"
#       routeKey                = "$context.routeKey"
#       status                  = "$context.status"
#       responseLength          = "$context.responseLength"
#       integrationErrorMessage = "$context.integrationErrorMessage"
#       }
#     )
#   }
#   depends_on = [aws_cloudwatch_log_group.api_gw]
# }

# resource "aws_apigatewayv2_integration" "apigw_lambda" {
#   api_id = aws_apigatewayv2_api.http_lambda.id

#   integration_uri    = aws_lambda_function.apigw_lambda_ddb.invoke_arn
#   integration_type   = "AWS_PROXY"
#   integration_method = "POST"
# }

# resource "aws_apigatewayv2_route" "post" {
#   api_id = aws_apigatewayv2_api.http_lambda.id

#   route_key = "POST /paste"
#   target    = "integrations/${aws_apigatewayv2_integration.apigw_lambda.id}"
# }

# resource "aws_cloudwatch_log_group" "api_gw" {
#   name = "/aws/api_gw/${var.app_name}-${random_string.random.id}"

#   retention_in_days = var.log_retention
# }

# resource "aws_lambda_permission" "api_gw" {
#   statement_id  = "AllowExecutionFromAPIGateway"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.apigw_lambda_ddb.function_name
#   principal     = "apigateway.amazonaws.com"

#   source_arn = "${aws_apigatewayv2_api.http_lambda.execution_arn}/*/*"
# }
