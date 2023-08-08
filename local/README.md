# set yourself up to develop on your local machine

## pre-requisites

### awscli

**awscli is required**

configure awscli for this use case (use profiles if you use awscli on other
projects!)

```bash
aws configure

# aws_access_key_id = 'X'
# aws_secret_access_key = 'X'
# region = 'local'
```

- Docker desktop engine installed and running

## dynamo db running on Docker

run the database locally (in a Docker container)

```bash
docker compose up
```

print out a list of tables in your DynamoDB instance:

```bash
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

expect to find the "paste" table:

```json
{
  "TableNames": ["paste"]
}
```

### stopping and removing dynamodb-local

**use `-v` flag to completely delete database table "paste"**

```bash
docker compose down -v
```

more info/examples: <https://github.com/aws-samples/aws-sam-java-rest>
