import json
import boto3

from .processor import process_document

s3 = boto3.client(
    "s3",
    region_name="ap-south-1"
)


def lambda_handler(event, context):

    print(json.dumps(event))

    for record in event["Records"]:

        body = json.loads(record["body"])

        s3_record = body["Records"][0]["s3"]

        bucket = s3_record["bucket"]["name"]

        key = s3_record["object"]["key"]

        print(bucket)
        print(key)

        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        text = response["Body"].read().decode()

        client_id = key.split("/")[0]

        chunks = process_document(
            client_id,
            text
        )

        print(f"Processed {chunks} chunks")

    return {
        "statusCode": 200
    }