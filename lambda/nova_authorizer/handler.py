# import json

# VALID_KEYS = {
#     "fintech-key": "fintech",
#     "healthcare-key": "healthcare",
#     "store-key": "store"
# }


# def handler(event, context):

#     api_key = event.get("headers", {}).get(
#         "x-api-key"
#     )

#     if api_key in VALID_KEYS:

#         return {
#             "isAuthorized": True,
#             "context": {
#                 "client_id": VALID_KEYS[api_key]
#             }
#         }

#     return {
#         "isAuthorized": False
#     }

import json

VALID_KEYS = {
    "fintech-key": "fintech",
    "healthcare-key": "healthcare",
    "store-key": "store"
}


def handler(event, context):

    print("AUTHORIZE EVENT:")
    print(json.dumps(event))

    headers = event.get("headers") or {}

    api_key = (
        headers.get("x-api-key")
        or headers.get("X-Api-Key")
        or headers.get("X-API-Key")
    )

    method_arn = event.get("methodArn", "*")

    if api_key not in VALID_KEYS:
        return {
            "principalId": "unauthorized",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Deny",
                        "Resource": method_arn
                    }
                ]
            }
        }

    client_id = VALID_KEYS[api_key]

    return {
        "principalId": client_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": method_arn
                }
            ]
        },
        "context": {
            "client_id": client_id
        }
    }