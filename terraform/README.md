# Terraform Instructions

## setup
To begin, move into the *terraform* directory with `cd terraform` \
Then, create a file to hold the secret variables in, called `terraform.tfvars`, using the command: `touch terraform.tfvars`
Inside this file, create the following variables in the form:

```
AWS_DEFAULT_REGION    = "<THE REGION OF CHOICE>"
AWS_ACCESS_KEY_ID     = "<YOUR AWS ACCESS KEY ID HERE>"
AWS_SECRET_ACCESS_KEY = "<YOUR SECRET AWS KEY HERE>"
VPC_ID                = "<YOUR VPC OF CHOICE HERE>"
CLUSTER_NAME          = "<YOUR CLUSTER NAME HERE>"

DB_DRIVER   = "<THE DB DRIVER NAME>"
DB_HOST     = "<THE HOST LINK TO THE RDS>"
DB_USERNAME = "<THE USERNAME OF THE USER>"
DB_PASSWORD = "<THE PASSWORD OF THE USER>"
DB_NAME     = "<THE NAME OF THE DATABASE>"

S3_BUCKET = "<THE NAME OF THE S3 BUCKET TO ARCHIVE TO>"
```

Next, run the following commands in the following order:

1. `terraform init` - This initialises the directory for terraform usage.
2. `terraform apply` -> `yes` - This applies the changes and begins to create the resources described.
3. *Important info:* The previous command should fail. This is because if terraform has not yet been ran, and no resources exist on the cloud yet, the terraform code which references the ECR repository will as of now reference nothing. To fix this, you will need to push the relevant images to the respective ECR repositories so they can be referenced.
4. *Push relevant images* - As described before, run each of the 3 dockerfile bash scripts to push the images to the correct repositories.
5. `terraform apply` -> `yes` - If all goes well, this should run fine, creating the desired resources.

## List of terraform resources main.tf will create:
- aws_ecr_repository | charn-pipeline-repo: The ECR repository for the pipeline container.
- aws_ecr_repository | charn-archive-repo: The ECR repository for the archive container.
- aws_ecr_repository | charn-dashboard-repo: The ECR repository for the dashboard container.
- aws_lb | c21-charn-ecs-load-balancer: The load balancer which directs traffic to the dashboard hosted on the ECS Service.
- aws_lb_listener | c21-charn-lb-listener: The load balancer listener which listens for traffic and forwards to the load balancer.
- aws_lb_target_group | c21-charn-target-group: The target group for the load balancer.
- aws_iam_policy | lambda-role-permissions-policy-pipeline: The policy allowing the lambda function full access to RDS.
- aws_iam_policy | lambda-role-permissions-policy-archive: The policy allowing the lambda function full access to RDS and s3.
- aws_iam_policy | task-definition-role-permissions-policy-dashboard: The policy allowing the task definition to access ECR.
- aws_iam_role | lambda-minute-role: The IAM role holding the relevant policies.
- aws_iam_role | lambda-daily-role: The IAM role holding the relevant policies.
- aws_iam_role | eventbridge-pipeline-scheduler-role: The IAM role allowing access to the eventbridge scheduler for minutely updates.
- aws_iam_role | eventbridge-pipeline-archive-role: The IAM role allowing access to the eventbridge scheduler for daily updates.
- aws_iam_role | ecs-execution-dashboard-role: The IAM role allowing the ecs tasks to be executed.
- aws_iam_role | ecs-task-definition-role-dashboard: The IAM role allowing the task definition to access ECR.
- aws_iam_policy_attachment | lambda-pipeline-role-policy-connection: Attaches the pipeline policy to the lambda role.
- aws_iam_policy_attachment | lambda-archive-role-policy-connection: Attaches the archive policy to the lambda role.
- aws_iam_policy_attachment | ecs-execution-dashboard-role-policy-connection: Attaches the task definition policy to the ECS role.
- aws_iam_role_policy | eventbridge-pipeline-role: The policy allowing the scheduler to invoke the pipeline lambda function.
- aws_iam_role_policy | eventbridge-archive-role: The policy allowing the scheduler to invoke the archive lambda function.
- aws_ecs_task_definition | ecs-dashboard-task-definition: The task definition which will be ran on the ECS Service, hosting the dashboard.
- aws_ecs_service | ecs-dashboard-service: The ECS service running the dashboard task at all times, on port 8501.
- aws_lambda_function | charn-pipeline-lambda: The pipeline lambda function itself, which will run the pipeline ECR container.
- aws_lambda_function | charn-archive-lambda: The lambda function itself, which will run the archive ECR container.
- aws_scheduler_schedule | c21-charn-pipeline-schedule: The pipeline eventbridge schedule, triggering the lambda every minute on a cron-based schedule.
- aws_scheduler_schedule | c21-charn-archive-schedule: The archive eventbridge schedule, triggering the lambda every day at 11:59pm on a cron-based schedule.
- aws_s3_bucket | c21-charn-archive-bucket: The s3 bucket in which the archived data from the RDS database is uploaded to and eventually hosted on the dashboard.

