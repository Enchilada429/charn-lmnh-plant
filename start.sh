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


log "🌱 Running first terraform apply (this may fail on fresh setup)..."
set +e
terraform apply -auto-approve
TF_EXIT_CODE=$?
set -e


log "🌱 Building & pushing pipeline image..."
cd "$PIPELINE_DIR"
./dockerise.sh
cd ..


log "🌱 Building & pushing dashboard image..."
cd "$DASHBOARD_DIR"
./dockerise.sh
cd ..


log "🌱 Building & pushing archived data image..."
cd "$ARCHIVE_DIR"
./dockerise.sh
cd ..


log "🌱 Running second terraform apply..."
cd "$TERRAFORM_DIR"
terraform apply -auto-approve


log "🪷 All done! Infrastructure and images are fully deployed."
