# Terraform Instructions

## setup
To begin, move into the *terraform* directory with `cd terraform` \
Next, run the following commands in the following order:

1. `terraform init` - This initialises the directory for terraform usage.
2. `terraform plan` - This is a check to see that the terraform will not run into any issues, and give an overview of the resources it will create/change.
3. `terraform apply` -> `yes` - This applies the changes and begins to create the resources described
4. *Important info:* The previous command should fail. This is because if terraform has not yet been ran, and no resources exist on the cloud yet, the terraform code which references the ECR repository will as of now reference nothing. To fix this, simply run the same command again.
5. `terraform apply` -> `yes` - If all goes well, this should run fine, creating the desired resources.

## List of terraform resources main.tf will create:
- aws_ecr_repository | charn-pipeline-repo: The ECR repository for the pipeline container.
- aws_iam_role | lambda-minute-role: The IAM role holding the relevant policies.
- aws_iam_policy | lambda-role-permissions-policy: The policy allowing the lambda function full access to RDS.
- aws_iam_policy_attachment | lambda-role-policy-connection: Attaches the policy to the lambda role.
- aws_lambda_function | charn-pipeline-lambda: The lambda function itself, which will run the ECR container.
- aws_iam_role | eventbridge-pipeline-scheduler-role: The IAM role allowing access to the eventbridge scheduler.
- aws_iam_role_policy | eventbridge-pipeline-role: The policy allowing the scheduler to invoke lambda functions.
- aws_scheduler_schedule | c21-charn-pipeline-schedule: The  pipeline eventbridge schedule, triggering the lambda every minute on a cron-based schedule.

