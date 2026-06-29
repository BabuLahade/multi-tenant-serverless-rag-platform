import json

from rag import ask


def handler(event, context):

    body = json.loads(
        event["body"]
    )

    question = body["message"]

    client_id = body["client_id"]

    result = ask(
        client_id,
        question
    )

    return {
        "statusCode": 200,

        "headers": {
            "Content-Type":
            "application/json"
        },

        "body": json.dumps(result)
    }