# def handler(event, context):

#     return {
#         "statusCode": 200,
#         "body": "Lambda Working"
#     }

import json
import os
import boto3

sqs = boto3.client('sqs')
# Ensure this matches the environment variable defined in your Terraform lambda module
QUEUE_URL = os.environ.get('SQS_QUEUE_URL') 

def handler(event, context):
    raw_body = event.get("body", "{}")
    if event.get("isBase64Encoded"):
        import base64
        raw_body = base64.b64decode(raw_body).decode("utf-8")

    try:
        body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Invalid JSON"})
        }

    client_id = body.get("client_id")
    url = body.get("url")

    if not client_id or not url:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "client_id and url required"})
        }

    if not QUEUE_URL:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "SQS_QUEUE_URL environment variable is missing"})
        }

    # Push the crawl job to SQS
    try:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({"client_id": client_id, "url": url})
        )
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"status": "successfully queued", "client_id": client_id, "url": url})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": f"Failed to queue message: {str(e)}"})
        }