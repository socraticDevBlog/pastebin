import json

import os

from model import Paste, PasteDataAware
from dynamodb import DB


class Configs:
    """

    Configs

    object used to build and store configuration values

    """

    def __init__(self, environ):
        self.is_local = environ["AWS_SAM_LOCAL"] == "true"
        self.region = "local" if self.is_local else "ca-central-1"
        self.dynamodb_endpoint = (
            self._dynamodb_endpoint_by_os(environ["DEVENV"]) if self.is_local else ""
        )

    def _dynamodb_endpoint_by_os(self, os: str):
        """

        Args:
            os (str): friendly name of the Operating System on which you are
            running Docker-engine/Desktop

        Returns:
            str: local Docker-based dynamodb endpoint
        """
        if os == "linux":
            return "http://localhost:8000"

        return "http://host.docker.internal:8000"


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

    configs = Configs(environ=os.environ)
    db = DB(
        is_local=configs.is_local,
        region=configs.region,
        dynamodb_endpoint_url=configs.dynamodb_endpoint,
    )

    if method == "GET":
        paste = PasteDataAware(db=db, id=event["queryStringParameters"]["id"])

        try:
            content = paste.read()
        except:
            return {"statusCode": 404}

        return {
            "statusCode": 200,
            "body": json.dumps({"content": content}),
        }
    elif method == "POST":
        paste = PasteDataAware(content=event["content"], db=db)

        try:
            id = paste.insert()
        except Exception as e:
            return {"statusCode": 500, "body": e.args[0]}

        return {
            "statusCode": 201,
            "body": json.dumps({"id": id}),
        }
    else:
        # APi Gateway should prevent this code for ever getting executed
        # (see template.yml definition file)
        return {"statusCode": 405, "body": json.dumps({"message": "bob"})}
