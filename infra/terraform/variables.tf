variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "use_localstack" {
  description = "Use LocalStack for local testing"
  type        = bool
  default     = true
}

variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "coding-agent-eval"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}
