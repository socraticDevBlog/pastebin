#!/bin/sh

#==============================================================================
#
#         FILE:  enable-ttl.sh
#
#        USAGE:  ./enable-ttl.sh
#
#  DESCRIPTION:  Enables TTL feature for dynamoDB table 'paste' locally
#
#      OPTIONS:  ---
# REQUIREMENTS:  TTL feature should work for developers locally
#         BUGS:  Describe any known bugs here.
#        NOTES:  Any additional notes go here.
#       AUTHOR:  socraticDev
#      COMPANY:  Your Company Name
#      VERSION:  1.0
#      CREATED:  2024-06-03
#     REVISION:  ---
#
#==============================================================================

tableName="paste"

# shellcheck disable=SC2148
aws dynamodb update-time-to-live \
    --endpoint-url http://localhost:8000 \
    --table-name "${tableName}" \
    --time-to-live-specification "Enabled=true, AttributeName=ttl"

aws dynamodb describe-time-to-live \
    --table-name "${tableName}" \
    --endpoint-url http://localhost:8000
