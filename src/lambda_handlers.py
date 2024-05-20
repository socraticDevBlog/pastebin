import json
from api_handler import ApiHandler


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
