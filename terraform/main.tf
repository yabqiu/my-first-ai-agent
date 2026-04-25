terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.42.0"
    }
  }
  backend "s3" {
    bucket = "yanbin-data"
    key = "ai-agent/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

# IAM Role
resource "aws_iam_role" "lambda_role" {
  name = "my-ai-agent-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "s3_policy" {
  name = "my-ai-agent-s3-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:PutObject"]
        Resource = "arn:aws:s3:::yanbin-data/ai-agent/found_cat_ids.txt"
      }
    ]
  })
}

resource "aws_iam_role_policy" "bedrock_policy" {
  name = "my-ai-agent-bedrock-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "bedrock:InvokeModel"
        Resource = "arn:aws:bedrock:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function
resource "aws_lambda_function" "my_ai_agent" {
  function_name    = "my-ai-agent"
  role             = aws_iam_role.lambda_role.arn
  runtime          = "python3.13"
  memory_size = 1024
  timeout = 300
  handler          = "my_first_ai_agent.lambda_function.handler"
  filename         = "../src/Archive.zip"
  source_code_hash = filebase64sha256("../src/Archive.zip")

  environment {
    variables = {
      PYTHONPATH         = "libs"
      TELEGRAM_BOT_TOKEN = var.telegram_bot_token
      TELEGRAM_CHAT_ID   = var.telegram_chat_id
    }
  }
}

# EventBridge Scheduler
resource "aws_scheduler_schedule" "daily_trigger" {
  name = "my-ai-agent-schedule"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = "cron(30 6,9 * * ? *)"
  schedule_expression_timezone = "America/Chicago"

  target {
    arn      = aws_lambda_function.my_ai_agent.arn
    role_arn = aws_iam_role.scheduler_role.arn
  }
}

resource "aws_iam_role" "scheduler_role" {
  name = "my-ai-agent-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "scheduler.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "scheduler_invoke_policy" {
  name = "my-ai-agent-scheduler-invoke-policy"
  role = aws_iam_role.scheduler_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "lambda:InvokeFunction"
      Resource = aws_lambda_function.my_ai_agent.arn
    }]
  })
}