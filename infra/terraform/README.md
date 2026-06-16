# D1 — Terraform Infrastructure

Terraform configuration for S3 bucket + Lambda + API Gateway.

## Prerequisites

- Terraform >= 1.5
- Optional: LocalStack for local testing (`docker run -p 4566:4566 localstack/localstack`)

## Commands

```bash
# Create placeholder Lambda zip
cd infra/terraform
zip lambda_placeholder.zip lambda/index.js 2>/dev/null || (mkdir -p lambda && echo 'exports.handler=async()=>({statusCode:200,body:"ok"})' > lambda/index.js && zip lambda_placeholder.zip lambda/index.js)

terraform init
terraform validate
terraform plan
```

## Apply / Destroy

```bash
terraform apply    # requires real AWS credentials or LocalStack
terraform destroy
```

## Resources

| Resource | Purpose |
|----------|---------|
| `aws_s3_bucket.data` | Data storage bucket |
| `aws_lambda_function.processor` | Event processor |
| `aws_apigatewayv2_api.api` | HTTP API Gateway |
| IAM roles/policies | Lambda execution permissions |
