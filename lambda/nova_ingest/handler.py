# # import json
# # import boto3

# # from  processor import process_document

# # s3 = boto3.client(
# #     "s3",
# #     region_name="ap-south-1"
# # )


# # def handler(event, context):

# #     print(json.dumps(event))

# #     for record in event["Records"]:

# #         body = json.loads(record["body"])

# #         s3_record = body["Records"][0]["s3"]

# #         bucket = s3_record["bucket"]["name"]

# #         key = s3_record["object"]["key"]

# #         print(bucket)
# #         print(key)

# #         response = s3.get_object(
# #             Bucket=bucket,
# #             Key=key
# #         )

# #         text = response["Body"].read().decode()

# #         client_id = key.split("/")[0]

# #         chunks = process_document(
# #             client_id,
# #             text
# #         )

# #         print(f"Processed {chunks} chunks")

# #     return {
# #         "statusCode": 200
# #     }

# import json
# import boto3

# from processor import process_document


# s3 = boto3.client(
#     "s3",
#     region_name="ap-south-1"
# )


# def handler(event, context):

#     print(json.dumps(event))

#     for record in event["Records"]:

#         body = json.loads(record["body"])

#         # Ignore the S3 notification test event
#         if body.get("Event") == "s3:TestEvent":
#             print("Ignoring S3 test event")
#             continue

#         s3_record = body["Records"][0]["s3"]

#         bucket = s3_record["bucket"]["name"]

#         key = s3_record["object"]["key"]

#         print(bucket)
#         print(key)

#         response = s3.get_object(
#             Bucket=bucket,
#             Key=key
#         )

#         text = response["Body"].read().decode()

#         client_id = key.split("/")[0]

#         chunks = process_document(
#             client_id,
#             text
#         )

#         print(f"Processed {chunks} chunks")

#     return {
#         "statusCode": 200
#     }

import json
import requests
from bs4 import BeautifulSoup
from processor import process_document

def handler(event, context):
    print("===== SQS EVENT RECEIVED =====")
    print(json.dumps(event))

    for record in event.get("Records", []):
        try:
            body = json.loads(record["body"])
            
            client_id = body.get("client_id")
            url = body.get("url")

            if not client_id or not url:
                print(f"Skipping malformed message: {body}")
                continue

            print(f"Ingesting URL: {url} for client: {client_id}")

            # 1. Fetch HTML from the URL
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # 2. Extract and clean text using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)

            # 3. Process, chunk, embed, and save to DynamoDB
            chunks_processed = process_document(client_id, text)

            print(f"Successfully processed {chunks_processed} chunks from {url}")

        except Exception as e:
            print(f"Error processing record: {str(e)}")
            # Raise exception so SQS marks it as failed and routes it to the DLQ
            raise e

    return {
        "statusCode": 200
    }