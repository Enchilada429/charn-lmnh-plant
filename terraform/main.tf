# provider

provider "aws" {
  region     = var.AWS_DEFAULT_REGION
  secret_key = var.AWS_SECRET_ACCESS_KEY
  access_key = var.AWS_ACCESS_KEY_ID
}   


## ECR for the pipeline lambda function

resource "aws_ecr_repository" "charn-pipeline-ecr" {
  name                 = "c21-charn-pipeline-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# references the ecr image which should be pushed to the repository
data "aws_ecr_image" "lambda-image-version" {
  repository_name = aws_ecr_repository.charn-pipeline-ecr.name
  image_tag       = "latest"
}

# Permissions etc. for the Lambda

# Trust doc (who is allowed to use this)
data "aws_iam_policy_document" "lambda-role-trust-policy-doc" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = [
      "sts:AssumeRole"
    ]
  }
}

data "aws_iam_policy_document" "lambda-role-permissions-policy-doc" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:eu-west-2:129033205317:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "rds:*"
    ]
    resources = ["*"]
  }
}

# Role (thing that can be assumed to get power)
resource "aws_iam_role" "lambda-minute-role" {
  name               = "c21-charn-pipeline-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

# Permissions policy
resource "aws_iam_policy" "lambda-role-permissions-policy" {
  name   = "c21-charn-pipeline-permissions-policy"
  policy = data.aws_iam_policy_document.lambda-role-permissions-policy-doc.json
}

# Connect the policy to the role
resource "aws_iam_role_policy_attachment" "lambda-role-policy-connection" {
  role       = aws_iam_role.lambda-minute-role.name
  policy_arn = aws_iam_policy.lambda-role-permissions-policy.arn
}

resource "aws_lambda_function" "charn-pipeline-lambda" {
  function_name = "c21-charn-pipeline"
  role          = aws_iam_role.lambda-minute-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.lambda-image-version.image_uri
  timeout       = 300
  memory_size   = 512
}


# eventbridge scheduler role
resource "aws_iam_role" "eventbridge-pipeline-scheduler-role" {
  name = "c21-charn-pipeline-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Effect = "Allow"
        Principal = {
            Service = "scheduler.amazonaws.com"
        }
        Action = "sts:AssumeRole"
    }]
  })
}


# eventbridge iam role policy
resource "aws_iam_role_policy" "eventbridge-pipeline-role" {
  policy = jsonencode({
    Statement = [{
        Action = "lambda:InvokeFunction"
        Effect = "Allow"
        Resource = aws_lambda_function.charn-pipeline-lambda.arn
    }]
  })
  role = aws_iam_role.eventbridge-pipeline-scheduler-role.id
}


# Eventbridge minute schedule
resource "aws_scheduler_schedule" "c21-charn-pipeline-schedule" {
  name = "c21-charn-pipeline-schedule"

  flexible_time_window {
    mode = "OFF"
  }
  
  schedule_expression = "cron(* * * * *)"

  target {
    arn = aws_lambda_function.charn-pipeline-lambda.arn
    role_arn = aws_iam_role.eventbridge-pipeline-scheduler-role.arn
  }
}


