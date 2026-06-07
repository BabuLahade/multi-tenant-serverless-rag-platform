import json

VALID_KEYS = {
    "fintech-key": "fintech",
    "healthcare-key": "healthcare",
    "store-key": "store"
}


def handler(event, context):

    api_key = event.get("headers", {}).get(
        "x-api-key"
    )

    if api_key in VALID_KEYS:

        return {
            "isAuthorized": True,
            "context": {
                "client_id": VALID_KEYS[api_key]
            }
        }

    return {
        "isAuthorized": False
    }