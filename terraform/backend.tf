# GitHub Action to use -backend parameters 
terraform {
  backend "s3" {
    workspace_key_prefix = "tfstate"
  }
}