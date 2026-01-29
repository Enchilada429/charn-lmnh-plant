# provider

provider "aws" {
  region     = var.AWS_DEFAULT_REGION
  secret_key = var.AWS_SECRET_ACCESS_KEY
  access_key = var.AWS_ACCESS_KEY_ID
}   

################### VPC ###################

# cohort 21 vpc
data "aws_vpc" "cohort-vpc" {
    id = var.VPC_ID
}
###########################################


################### Subnets ###################

data "aws_subnets" "public-subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.cohort-vpc.id]
  }

  filter {
    name   = "tag:Name"
    values = ["c21-public-subnet-*"]
  }
}
###############################################


################### ECR repositories ###################

# repo for the pipeline lambda function
resource "aws_ecr_repository" "charn-pipeline-ecr" {
  name                 = "c21-charn-pipeline-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  force_delete = true
}

# repo for the archive lambda function
resource "aws_ecr_repository" "charn-archive-ecr" {
  name                 = "c21-charn-archive-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  force_delete = true
}

# repo for the dashboard ecs service
resource "aws_ecr_repository" "charn-dashboard-ecr" {
  name                 = "c21-charn-dashboard-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  force_delete = true
}
########################################################


################### ECS Cluster ###################

data "aws_ecs_cluster" "c21-cluster" {
  cluster_name = var.CLUSTER_NAME
}
###################################################


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

# references the ecs-image-dashboard
data "aws_ecr_image" "ecs-image-dashboard" {
    repository_name = aws_ecr_repository.charn-dashboard-ecr.name
    image_tag =  "latest"
}

################################################## 


################### Load Balancer / Listener ################### 

# load balancer for ECS dashboard service
resource "aws_lb" "c21-charn-ecs-load-balancer" {
  name = "c21-charn-ecs-load-balancer"
  internal = false
  load_balancer_type = "application"
  subnets = data.aws_subnets.public-subnets.ids
  
  
}

# listener for load balancer
resource "aws_lb_listener" "c21-charn-lb-listener" {
  load_balancer_arn = aws_lb.c21-charn-ecs-load-balancer.arn
  port = 8502
  protocol = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.c21-charn-target-group.id
  }
}
##################################################### 


################### LB Target Group ################### 

# target group for the load balancer
resource "aws_lb_target_group" "c21-charn-target-group" {
  name = "c21-charn-target-group"
  port = 8502
  protocol = "HTTP"
  target_type = "ip"
  vpc_id = data.aws_vpc.cohort-vpc.id
}

# data "aws_lb_target_group" "c21-charn-lb-target-group" {
#   name = "c21-charn-target-group"
# }
######################################################## 


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

# ECR permissions for policy document
data "aws_iam_policy_document" "ecs-role-permissions-policy-doc-dashboard" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
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

resource "aws_iam_policy" "task-definition-role-permissions-policy-dashboard" {
  name   = "c21-charn-dashboard-permissions-policy"
  policy = data.aws_iam_policy_document.ecs-role-permissions-policy-doc-dashboard.json
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

# ecs execution dashboard role
resource "aws_iam_role" "ecs-execution-dashboard-role" {
  name = "c21-charn-ecs-execution-dashboard-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Effect = "Allow"
        Principal = {
            Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
    }]
  })
}

# ecs task definition role
resource "aws_iam_role" "ecs-task-definition-role-dashboard" {
  name = "c21-charn-ecs-task-definition-role-dashboard"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
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

# Connect the task definition policy to the ecs role
resource "aws_iam_role_policy_attachment" "ecs-execution-dashboard-role-policy-connection" {
  role       = aws_iam_role.ecs-execution-dashboard-role.name
  policy_arn = aws_iam_policy.task-definition-role-permissions-policy-dashboard.arn
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
  role = aws_iam_role.eventbridge-archive-scheduler-role.id
}
##################################################### 


################### ECS Task Definition ################### 

# ecs dashboard task definition
resource "aws_ecs_task_definition" "ecs-dashboard-task-definition" {
  family = "c21-charn-dashboard-task-definition"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn = aws_iam_role.ecs-execution-dashboard-role.arn
  task_role_arn = aws_iam_role.ecs-task-definition-role-dashboard.arn
  network_mode = "awsvpc"
  cpu = "1024"
  memory = "2048"

  runtime_platform {
      operating_system_family = "LINUX"
      cpu_architecture = "X86_64"
    }

  container_definitions = jsonencode([
    {
        name = "c21-charn-dashboard-container"
        image = data.aws_ecr_image.ecs-image-dashboard.image_uri
        cpu = 1024
        memory = 2048
        essential = true
        portMappings = [
            {
                containerPort = 8502
                hostPort = 8502
            }
        ]

        environment = [
            {
                name  = "DB_HOST"
                value = var.DB_HOST
            },
            {
                name  = "DB_PORT"
                value = "1433"
            },
            {
                name  = "DB_USERNAME"
                value = var.DB_USERNAME
            },
            {
                name  = "DB_PASSWORD"
                value = var.DB_PASSWORD
            },
            {
                name  = "DB_NAME"
                value = var.DB_NAME
            },
            {
                name  = "AWS_SECRET_KEY"
                value = var.AWS_SECRET_ACCESS_KEY
            },
            {
                name  = "AWS_ACCESS_KEY"
                value = var.AWS_ACCESS_KEY_ID
            },
            {
                name  = "S3_BUCKET"
                value = var.S3_BUCKET
            },
        ]
    }
  ])
}
############################################################ 


################### ECS Service ################### 

# dashboard service
resource "aws_ecs_service" "ecs-dashboard-service" {
  name                               = "c21-charn-dashboard-service"
  cluster                            = data.aws_ecs_cluster.c21-cluster.id
  task_definition                    = aws_ecs_task_definition.ecs-dashboard-task-definition.arn
  launch_type                        = "FARGATE"
  platform_version                   = "LATEST"
  desired_count                      = 1
  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 0
  depends_on                         = [aws_lb_listener.c21-charn-lb-listener]

  load_balancer {
    target_group_arn = aws_lb_target_group.c21-charn-target-group.arn
    container_name = "c21-charn-dashboard-container"
    container_port = 8502
  }

  network_configuration {
    subnets = data.aws_subnets.public-subnets.ids
    assign_public_ip = true
  }
}
#################################################### 


################### Lambda Functions ################### 

# minutely pipeline lambda function
resource "aws_lambda_function" "charn-pipeline-lambda" {
  function_name = "c21-charn-pipeline"
  role          = aws_iam_role.lambda-minute-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.lambda-image-pipeline.image_uri
  timeout       = 300
  memory_size   = 512

  environment {
    variables = {
        DB_DRIVER   = var.DB_DRIVER
        DB_HOST     = var.DB_HOST
        DB_NAME     = var.DB_NAME
        DB_USERNAME = var.DB_USERNAME
        DB_PORT     = "1433"
        DB_PASSWORD = var.DB_PASSWORD
    }
  }
}

# daily lambda archive function
resource "aws_lambda_function" "charn-archive-lambda" {
  function_name = "c21-charn-archive"
  role          = aws_iam_role.lambda-daily-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.lambda-image-archive.image_uri
  timeout       = 300
  memory_size   = 512

  environment {
    variables = {
        DB_DRIVER   = var.DB_DRIVER
        DB_HOST     = var.DB_HOST
        DB_NAME     = var.DB_NAME
        DB_USERNAME = var.DB_USERNAME
        DB_PORT     = "1433"
        DB_PASSWORD = var.DB_PASSWORD
        S3_BUCKET   = var.S3_BUCKET
    }
  }
}
######################################################## 


################### Eventbridge Schedules ################### 

# Eventbridge minutely pipeline schedule
resource "aws_scheduler_schedule" "c21-charn-pipeline-schedule" {
  name = "c21-charn-pipeline-schedule"

  flexible_time_window {
    mode = "OFF"
  }
  
  schedule_expression = "cron(* * * * ? *)"

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
  
  schedule_expression = "cron(59 23 * * ? *)"

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
#################################################


################### s3 Bucket Policy ###################

resource "aws_s3_bucket_policy" "c21-charn-public-bucket-policy" {
  bucket = aws_s3_bucket.c21-charn-archive-bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Sid = "PublicReadGetObject"
        Effect = "Allow"
        Principal = "*"
        Action = "s3:GetObject"
        Resource = [
            "arn:aws:s3:::c21-charn-archive-bucket/*"
        ]
    }
    ]
  })
}
########################################################


################### s3 Bucket Public Access Block ###################

resource "aws_s3_bucket_public_access_block" "c21-charn-archive-bucket-block" {
    bucket = aws_s3_bucket.c21-charn-archive-bucket.id

    block_public_acls = false
    block_public_policy = false
    ignore_public_acls = false
    restrict_public_buckets = false
}
#####################################################################