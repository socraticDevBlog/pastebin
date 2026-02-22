# GitHub Action to use -backend parameters 
# terraform init -backend-config="bucket=${AWS_BUCKET_NAME}"  -backend-config="key=${AWS_BUCKET_KEY_NAME}" -backend-config="region=${AWS_REGION}"

terraform {
  backend "s3" {
  }
}