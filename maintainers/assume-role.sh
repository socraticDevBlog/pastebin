#!/bin/bash

AWS_ACCOUNT_ID_NUMBER="YOU_AWS_ACCOUNT_ID_NUMBER_HERE"

## execute this script either:
##  source assume-role.sh
##  or
##  . assume-role.sh

unset "AWS_ACCESS_KEY_ID"
unset "AWS_SECRET_ACCESS_KEY"
unset "AWS_SESSION_TOKEN"

# Parse JSON input and extract required values
parse_json() {
    local json=$1
    local key=$2
    local value=$(echo "$json" | jq -r ".$key")
    echo "$value"
}

# Read JSON input from command's output
json_input=$(aws sts assume-role --role-arn arn:aws:iam::"${AWS_ACCOUNT_ID_NUMBER}":role/github-action-terraform-oidc --role-session-name "dev-local")

# Extract required values
access_key_id=$(parse_json "$json_input" "Credentials.AccessKeyId")
secret_access_key=$(parse_json "$json_input" "Credentials.SecretAccessKey")
session_token=$(parse_json "$json_input" "Credentials.SessionToken")

# Export values to environment variables
export AWS_ACCESS_KEY_ID="$access_key_id"
export AWS_SECRET_ACCESS_KEY="$secret_access_key"
export AWS_SESSION_TOKEN="$session_token"

# Print exported variables for verification
echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID"
echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY"
echo "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN"
