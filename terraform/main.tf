# provider

provider "aws" {
  region     = var.AWS_DEFAULT_REGION
  secret_key = var.AWS_SECRET_ACCESS_KEY
  access_key = var.AWS_ACCESS_KEY_ID
}   


################### ECR repositories ###################

# repo for the pipeline lambda function
resource "aws_ecr_repository" "charn-pipeline-ecr" {
  name                 = "c21-charn-pipeline-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# repo for the archive lambda function
resource "aws_ecr_repository" "charn-archive-ecr" {
  name                 = "c21-charn-archive-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
########################################################


################### ECR Images ###################

# references the pipeline ecr image which should be pushed to the repository
data "aws_ecr_image" "lambda-image-pipeline" {
  repository_name = aws_ecr_repository.charn-pipeline-ecr.name
  image_tag       = "latest"
}

# references the archive ecr image
data "aws_ecr_image" "lambda-image-archive" {
    repository_name = aws_ecr_repository.charn-archive-ecr.name
    image_tag       = "latest"
}
##################################################


################### Policy Documents ###################

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

# RDS permissions policy document
data "aws_iam_policy_document" "lambda-role-permissions-policy-doc-pipeline" {
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

# RDS and s3 permissions policy document
data "aws_iam_policy_document" "lambda-role-permissions-policy-doc-archive" {
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

  statement {
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = ["*"]
  }
}
######################################################


################### Policies ###################

# Permissions policy
resource "aws_iam_policy" "lambda-role-permissions-policy-pipeline" {
  name   = "c21-charn-pipeline-permissions-policy"
  policy = data.aws_iam_policy_document.lambda-role-permissions-policy-doc-pipeline.json
}

resource "aws_iam_policy" "lambda-role-permissions-policy-archive" {
  name   = "c21-charn-archive-permissions-policy"
  policy = data.aws_iam_policy_document.lambda-role-permissions-policy-doc-archive.json
}
################################################


################### Roles ###################

# minutely pipeline lambda role
resource "aws_iam_role" "lambda-minute-role" {
  name               = "c21-charn-pipeline-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

# daily archive lambda role
resource "aws_iam_role" "lambda-daily-role" {
  name               = "c21-charn-archive-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

# eventbridge minutely pipeline scheduler role
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

# eventbridge daily archive scheduler role
resource "aws_iam_role" "eventbridge-archive-scheduler-role" {
  name = "c21-charn-archive-scheduler-role"

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
#############################################


################### Role-Policy Attachments ###################
# Connect the pipeline policy to the pipeline role
resource "aws_iam_role_policy_attachment" "lambda-pipeline-role-policy-connection" {
  role       = aws_iam_role.lambda-minute-role.name
  policy_arn = aws_iam_policy.lambda-role-permissions-policy-pipeline.arn
}

# Connect the archive policy to the archive role
resource "aws_iam_role_policy_attachment" "lambda-archive-role-policy-connection" {
  role       = aws_iam_role.lambda-daily-role.name
  policy_arn = aws_iam_policy.lambda-role-permissions-policy-archive.arn
}
###############################################################


################### Role Policies ###################

# eventbridge pipeline iam role policy
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

# eventbridge archive iam role policy
resource "aws_iam_role_policy" "eventbridge-archive-role" {
  policy = jsonencode({
    Statement = [{
        Action = "lambda:InvokeFunction"
        Effect = "Allow"
        Resource = aws_lambda_function.charn-archive-lambda.arn
    }]
  })
  role = aws_iam_role.eventbridge-pipeline-scheduler-role.id
}
#####################################################


################### Lambda Functions ###################

# minutely pipeline lambda function
resource "aws_lambda_function" "charn-pipeline-lambda" {
  function_name = "c21-charn-pipeline"
  role          = aws_iam_role.lambda-minute-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.lambda-image-pipeline.image_uri
  timeout       = 300
  memory_size   = 512
}

# daily lambda archive function
resource "aws_lambda_function" "charn-archive-lambda" {
  function_name = "c21-charn-archive"
  role          = aws_iam_role.lambda-daily-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.lambda-image-archive.image_uri
  timeout       = 300
  memory_size   = 512
}
########################################################


################### Eventbridge Schedules ###################

# Eventbridge minutely pipeline schedule
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

# Eventbridge daily pipeline schedule
resource "aws_scheduler_schedule" "c21-charn-archive-schedule" {
  name = "c21-charn-archive-schedule"

  flexible_time_window {
    mode = "OFF"
  }
  
  schedule_expression = "cron(0 18 * * *)"

  target {
    arn = aws_lambda_function.charn-archive-lambda.arn
    role_arn = aws_iam_role.eventbridge-archive-scheduler-role.arn
  }
}
#############################################################


################### s3 Bucket ###################

resource "aws_s3_bucket" "c21-charn-archive-bucket" {
  bucket = "c21-charn-archive-bucket"

  tags = {
    Name = "c21-charn-archive-bucket"
  }

  force_destroy = true
}
