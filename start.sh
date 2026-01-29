#!/usr/bin/env bash
source .env

TERRAFORM_DIR="./terraform"
PIPELINE_DIR="./pipeline"
DASHBOARD_DIR="./dashboard"
ARCHIVE_DIR="./archive"

log() {
    echo -e "\n🪷 $1\n"
}


log "🌱 Starting full infrastructure and deployment run..."


log "🌱 Running terraform init..."
cd "$TERRAFORM_DIR"
terraform init


log "🌱 Applying ECR repositories only..."
terraform apply -auto-approve \
    -target=aws_ecr_repository.c21-charn-pipeline-ecr \
    -target=aws_ecr_repository.c21-charn-dashboard-ecr \
    -target=aws_ecr_repository.c21-charn-archive-ecr

cd ..

log "🌱 Building & pushing pipeline image..."
cd "$PIPELINE_DIR"
sh ./dockerise.sh
cd ..


log "🌱 Building & pushing dashboard image..."
cd "$DASHBOARD_DIR"
sh ./dockerise.sh
cd ..


log "🌱 Building & pushing archive image..."
cd "$ARCHIVE_DIR"
sh ./dockerise.sh
cd ..


log "🌱 Applying remaining resources..."
cd "$TERRAFORM_DIR"
terraform apply -auto-approve


log "🪷 All done! Infrastructure and images are fully deployed."
