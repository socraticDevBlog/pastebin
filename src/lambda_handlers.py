import json
from api_handler import ApiHandler
from model import PasteDataAware


def get_handler(paste: PasteDataAware, is_web_browser: bool = False):
    try:
        content = paste.read()
    except:
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


def post_handler(paste: PasteDataAware):
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


def get_pastes_handler(api_handler: ApiHandler, client_id: str):
    paste_urls = api_handler.latest_pastes_urls(client_identifier=client_id)

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {
            "content-type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,GET,OPTIONS,DELETE",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(paste_urls),
    }
