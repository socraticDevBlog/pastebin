import json


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
    method = event["method"]
    message = event["message"]

    if method == "GET":
        return {
            "statusCode": 200,
            "body": json.dumps({"message": message}),
        }
    elif method == "POST":
        return {
            "statusCode": 201,
            "body": json.dumps({"message": message}),
        }
    else:
        return {"statusCode": 405, "body": json.dumps({"message": message})}
