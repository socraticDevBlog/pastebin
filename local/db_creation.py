import boto3

TABLE_NAME = "paste"

ENDPOINT_URL = "http://localhost:8000"

table_key_schema = [{"AttributeName": "ID", "KeyType": "HASH"}]
attribute_definitions = [
    {"AttributeName": "ID", "AttributeType": "S"},
]
provisioned_throughput = {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}

dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT_URL)
table = dynamodb.create_table(
    TableName=TABLE_NAME,
    KeySchema=table_key_schema,
    AttributeDefinitions=attribute_definitions,
    ProvisionedThroughput=provisioned_throughput,
)

table.wait_until_exists()

print("SUCCESS!!!")
