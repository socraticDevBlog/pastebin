import boto3
from typing import Dict


class DB_Exception(Exception):
    pass


class Not_Found(DB_Exception):
    pass


class DB:
    """
    DB

    specialized DynamoDB object that implements CRUD operations

    """

    def __init__(
        self,
        is_local: bool,
        dynamodb_endpoint_url: str = "",
        region: str = "us-east-1",
        table_name: str = "paste",
    ):
        if is_local:
            self._table = boto3.resource(
                "dynamodb", endpoint_url=dynamodb_endpoint_url
            ).Table(table_name)
        else:
            self._table = boto3.resource("dynamodb", region_name=region).Table(
                table_name
            )

    def insert(self, dict: Dict) -> str:
        """
        insert

        saves Paste into dynamoDB

        input: dictionary featuring a required "id" field of type string

        returns Paste's "id"

        """
        try:
            self._table.put_item(Item=dict)
        except:
            raise DB_Exception(f"Writing to table failed")

        return dict["id"]

    def get_item(self, id: str):
        """
        get_item

        fetches whole DynamoDB Item by key "id"

        returns whole DynamoDB Item

        """
        response = self._table.get_item(
            Key={"id": id},
        )

        if "Item" not in response:
            raise Not_Found

        return response

    def paste_ids_by_client_identifier(self, client_identifier: str, count: int = 5):
        """

        paste_ids_by_client_identifier

        fetches n Paste's ID from table based on a client_identifier

        client_identifier is by default client's IP address

        IDs are also sorted from most recent to less recent


        """
        response = self._table.scan(
            FilterExpression="metadata.client_identifier = :cid",
            ExpressionAttributeValues={":cid": client_identifier},
        )
        items = response["Items"]
        sorted_items = sorted(
            items, key=lambda x: x["created_time_epoch"], reverse=True
        )
        ret = []
        for x in sorted_items[:count]:
            ret.append(x["id"])

        return ret
