import json

from model import Paste


def lambda_handler(event, context):
    """
    lambda_handler

    Handles all http requests (from API Gateway)

    - receives requests
    - dispatch request to appropriate business logic
    - returns http "statusCode" + a "body" with either:
      a) "id" of a newly created Paste (GET)
      b) "content" of a retrieved Paste (POST)

    """
    method = event["httpMethod"]

    if method == "GET":
        paste = Paste(
            content="dummy content because Database is not plugged yet",
            id=event["queryStringParameters"]["id"],
        )
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"content": paste.dict()["content"], "pasteInfos": paste.dict()}
            ),
        }
    elif method == "POST":
        body = json.loads(event["body"])
        paste = Paste(content=body["content"])
        return {
            "statusCode": 201,
            "body": json.dumps({"id": paste.id}),
        }
    else:
        # APi Gateway should prevent this code for ever getting executed
        # (see template.yml definition file)
        return {"statusCode": 405, "body": json.dumps({"message": "bob"})}
