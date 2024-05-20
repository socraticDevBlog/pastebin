import json, os, hashlib
import logging

from model import PasteDataAware
from api_handler import ApiHandler
from dynamodb import DB
from lambda_handlers import get_pastes_handler

logger = logging.getLogger()
logger.setLevel("INFO")


def hash_value(value: str, encoding: str = "utf-8") -> str:
    value_bytes = str(value).encode(encoding=encoding)
    hash_object = hashlib.md5()
    hash_object.update(value_bytes)
    return hash_object.hexdigest()


def _dynamodb_endpoint_by_os(os: str):
    """

    Args:
        os (str): friendly name of the Operating System on which you are
        running Docker-engine/Desktop

    Returns:
        str: local Docker-based dynamodb endpoint
    """

    if os == "":
        return ""

    if os == "linux":
        return "http://localhost:8000"

    return "http://host.docker.internal:8000"


def get_handler(event, context, db: DB, is_web_browser: bool = False):
    try:
        id = event["queryStringParameters"]["id"]
        paste = PasteDataAware(db=db, id=id)
        content = paste.read()
    except:
        logger.error(f"GET-failed to retrieve requested paste-id {id}")
        return {"statusCode": 404}

    if is_web_browser:
        response_html = """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Saved Content</title>
                    <meta charset="UTF-8">
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
            "isBase64Encoded": paste.is_base64_encoded(content=content),
            "headers": {
                "Content-Type": "text/html; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS,DELETE",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": response_html,
        }

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


def post_handler(event, context, db: DB):
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
        logger.warning(f'POST- unable to load content from event["body"])["content"]')
        content = event["content"]

    client_id = ""
    try:
        client_id = json.loads(event["body"], strict=False)["client_id"]
    except:
        client_id = client_ip

    paste = PasteDataAware(
        content=content, db=db, client_identifier=hash_value(client_id)
    )

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


def options_handler(event, context):
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
    path = event["path"]

    is_local_envir = os.environ["AWS_SAM_LOCAL"] == "true"
    db = DB(
        is_local=is_local_envir,
        region="local" if is_local_envir else "ca-central-1",
        dynamodb_endpoint_url=_dynamodb_endpoint_by_os(os=os.environ["DEVENV"]),
    )

    api_handler = ApiHandler(db=db, base_url=os.environ.get("BASE_URL"))

    if method == "GET":
        if "/api/pastes" in path:
            query_params = event.get("queryStringParameters", {})

            try:
                client_id = query_params.get("client_id")
            except:
                client_id = event["requestContext"]["identity"]["sourceIp"]

            return get_pastes_handler(
                api_handler=api_handler,
                client_id=hash_value(client_id),
            )

        if "/api" in path:
            return get_handler(context=context, event=event, db=db)

        try:
            user_agent = event.get("headers", {}).get("User-Agent", "")
            is_web_browser = "Mozilla" in user_agent or "AppleWebKit" in user_agent
            return get_handler(
                context=context, event=event, db=db, is_web_browser=is_web_browser
            )
        except Exception as e:
            return get_handler(context=context, event=event, db=db)
    elif method == "POST":
        return post_handler(context=context, event=event, db=db)
    else:
        return options_handler(context=context, event=event)
