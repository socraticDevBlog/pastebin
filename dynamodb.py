import boto3
from typing import Dict

ENDPOINT_URL = "http://localhost:8000"


class DB:
    """
    DB

    specialized DynamoDB object that implements CRUD operations

    """

    def __init__(
        self, table_name: str = "paste", dynamodb_endpoint_url: str = ENDPOINT_URL
    ):
        db = boto3.resource("dynamodb", endpoint_url=dynamodb_endpoint_url)
        self._table = db.Table(table_name)
        self._db = db

    def create(self, dict: Dict) -> str:
        """
        create

        saves Paste into dynamoDB

        input: dictionary featuring a required "id" field of type string

        returns Paste's "id"

        """
        self._table.put_item(Item=dict)
        return dict["id"]

    def get_item(self, id: str):
        """
        get_item

        fetches whole DynamoDB Item by key "id"

        returns whole DynamoDB Item

        """
        return self._table.get_item(
            Key={"id": id},
        )
