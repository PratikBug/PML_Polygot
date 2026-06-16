output "s3_bucket_name" {
  value = aws_s3_bucket.data.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.processor.function_name
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.api.api_endpoint
}
