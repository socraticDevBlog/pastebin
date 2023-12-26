"""
(utils)
script to dump all items in local (Docker) dynamodb table

command: 

- pipenv shell
- cd local
- python boto-dynamodb-read.py

"""

import boto3

# Set the endpoint URL for the local DynamoDB instance
endpoint_url = "http://localhost:8000"

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)

# Specify the name of your DynamoDB table
table_name = "paste"

# Get the DynamoDB table
table = dynamodb.Table(table_name)

# Scan the table to retrieve all items
response = table.scan()

# Print the items
items = response.get("Items", [])
for item in items:
    print(item)
