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
endpointUrl="http://localhost:8000"

# shellcheck disable=SC2148
aws dynamodb update-time-to-live \
    --endpoint-url ${endpointUrl} \
    --table-name "${tableName}" \
    --time-to-live-specification "Enabled=true, AttributeName=ttl"

aws dynamodb describe-time-to-live \
    --endpoint-url ${endpointUrl} \
    --table-name "${tableName}"
