terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # LocalStack / test backend support
  skip_credentials_validation = var.use_localstack
  skip_requesting_account_id  = var.use_localstack
  skip_metadata_api_check     = var.use_localstack

  endpoints {
    s3         = var.use_localstack ? "http://localhost:4566" : null
    lambda     = var.use_localstack ? "http://localhost:4566" : null
    apigateway = var.use_localstack ? "http://localhost:4566" : null
    iam        = var.use_localstack ? "http://localhost:4566" : null
  }
}
