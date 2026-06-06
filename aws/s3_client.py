import boto3
import os
from botocore.exceptions import ClientError

BUCKET_NAME = "nova-raw-content"

s3 = boto3.client("s3")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def upload_file(local_file, s3_key):

    try:

        full_path = os.path.join(BASE_DIR, local_file)

        s3.upload_file(
            full_path,
            BUCKET_NAME,
            s3_key
        )

        print(f"Uploaded: {s3_key}")

    except ClientError as e:
        print(e)


if __name__ == "__main__":

    upload_file(
        "local-api/sample_docs/fintech.txt",
        "fintech/raw/fintech.txt"
    )