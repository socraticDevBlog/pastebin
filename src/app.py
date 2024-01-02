import json

import os

from model import PasteDataAware
from dynamodb import DB
import logging

logger = logging.getLogger()
logger.setLevel("INFO")


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
        try:
            paste = PasteDataAware(db=db, id=event["queryStringParameters"]["id"])
            content = paste.read()
        except:
            logger.error(f"GET-failed to retrieve requested paste-id {id}")
            return {"statusCode": 404}

        try:
            user_agent = event.get("headers", {}).get("User-Agent", "")
            is_web_browser = "Mozilla" in user_agent or "AppleWebKit" in user_agent
        except:
            is_web_browser = False

        if is_web_browser:
            response_html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Saved Content</title>
                </head>
                <body>
                    <pre>{}</pre>
                </body>
                </html>
            """.format(
                content
            )
            return {
                "statusCode": 200,
                "isBase64Encoded": False,
                "headers": {
                    "Content-Type": "text/html",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS,DELETE",
                    "Access-Control-Allow-Headers": "Content-Type",
                },
                "body": response_html,
            }
        else:
            return {
                "statusCode": 200,
                "isBase64Encoded": False,
                "headers": {
                    "content-type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS,DELETE",
                    "Access-Control-Allow-Headers": "Content-Type",
                },
                "body": json.dumps(content),
            }
    elif method == "POST":
        try:
            # Extract the IP address from the event
            client_ip = event["requestContext"]["identity"]["sourceIp"]
            logger.info(f"POST-client IP address: {client_ip}")
        except:
            logger.warn(
                "POST- client IP address not available at event['requestContext']['identity']['sourceIp']"
            )

        try:
            content = json.loads(event["body"], strict=False)["content"]
        except:
            logger.warning(
                f'POST- unable to load content from event["body"])["content"]'
            )
            content = event["content"]

        paste = PasteDataAware(content=content, db=db)

        try:
            id = paste.insert()
        except Exception as e:
            return {"statusCode": 500, "body": e.args[0]}

        return {
            "statusCode": 201,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS,DELETE",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps({"id": id}),
        }
    else:
        # APi Gateway should prevent this code for ever getting executed
        # (see template.yml definition file)
        return {
            "statusCode": 200,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS,DELETE",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps({"message": "probably checking your OPTIONS"}),
        }
