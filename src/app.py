import json

from paste import Paste


def lambda_handler(event, context):
    """
    lambda_handler

    Handles all http requests (from API Gateway)

    - receives requests
    - dispatch request to appropriate function
    - returns http "statusCode" + a "body" with at least:
      a) "message" field
      ...

    """
    method = event["httpMethod"]

    if method == "GET":
        paste = Paste(content="temp")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": paste.to_string()}),
        }
    elif method == "POST":
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "bob"}),
        }
    else:
        return {"statusCode": 405, "body": json.dumps({"message": "bob"})}
