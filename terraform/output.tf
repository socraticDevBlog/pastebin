output "lambda_arn" {
  value = aws_lambda_function.apigw_lambda_ddb.arn
}

output "lambda_s3_storage_id" {
  value = aws_s3_bucket.lambda_bucket.id
}

output "lambda_db_iam_policy" {
  value = aws_iam_policy.lambda_exec_role.arn
}

output "dynamo_db_arn" {
  value = aws_dynamodb_table.paste.arn
}

output "cloudwatch_log_group_arn" {
  value = aws_cloudwatch_log_group.lambda_logs.arn
}

output "api_gateway_endpoint" {
  value = aws_apigatewayv2_api.http_lambda.api_endpoint
}

output "api_gateway_arn" {
  value = aws_apigatewayv2_api.http_lambda.arn
}

output "api_gateway_route" {
  value = aws_apigatewayv2_route.get.route_key
}