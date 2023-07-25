# set yourself up to develop on your local machine

## pre-requisites

### awscli

**awscli is required**

configure awscli for this use case (use profiles if you use awscli on other
projects!)

```
aws configure

# aws_access_key_id = 'X'
# aws_secret_access_key = 'X'
# region = 'local'
```


- Docker desktop engine installed and running

## dynamo db running on Docker

run the database locally (in a Docker container)

````
docker pull amazon/dynamodb-local

docker run -p 8000:8000 amazon/dynamodb-local

````

run script `db_creation.py` once


print out a list of tables in your DynamoDB instance:
````
aws dynamodb list-tables --endpoint-url http://localhost:8000
````

more info/examples: https://github.com/aws-samples/aws-sam-java-rest

## SAM (serverless application model)

````bash
brew install aws-sam-cli
````
