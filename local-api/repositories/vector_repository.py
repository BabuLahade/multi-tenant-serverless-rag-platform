import boto3
from decimal import Decimal

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-south-1"
)

table = dynamodb.Table("nova-vectors")


def save_chunk(
    client_id,
    chunk_id,
    text,
    embedding
):

    embedding = [
        Decimal(str(x))
        for x in embedding
    ]

    table.put_item(
        Item={
            "client_id": client_id,
            "chunk_id": chunk_id,
            "text": text,
            "embedding": embedding
        }
    )

    print(
        f"Saved {client_id}:{chunk_id}"
    )