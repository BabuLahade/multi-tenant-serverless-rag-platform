import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-south-1"
)

table = dynamodb.Table("nova-vectors")


def save_test_item():

    response = table.put_item(
        Item={
            "client_id": "fintech",
            "chunk_id": "test001",
            "text": "hello dynamodb",
            
        }
    )

    print("Item inserted successfully")
    print(response["ResponseMetadata"]["HTTPStatusCode"])


if __name__ == "__main__":
    save_test_item()