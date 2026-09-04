# # # import json

# # # VALID_KEYS = {
# # #     "fintech-key": "fintech",
# # #     "healthcare-key": "healthcare",
# # #     "store-key": "store"
# # # }


# # # def handler(event, context):

# # #     api_key = event.get("headers", {}).get(
# # #         "x-api-key"
# # #     )

# # #     if api_key in VALID_KEYS:

# # #         return {
# # #             "isAuthorized": True,
# # #             "context": {
# # #                 "client_id": VALID_KEYS[api_key]
# # #             }
# # #         }

# # #     return {
# # #         "isAuthorized": False
# # #     }

# # import json

# # VALID_KEYS = {
# #     "fintech-key": "fintech",
# #     "healthcare-key": "healthcare",
# #     "store-key": "store"
# # }


# # def handler(event, context):

# #     print("AUTHORIZE EVENT:")
# #     print(json.dumps(event))

# #     headers = event.get("headers") or {}

# #     api_key = (
# #         headers.get("x-api-key")
# #         or headers.get("X-Api-Key")
# #         or headers.get("X-API-Key")
# #     )

# #     method_arn = event.get("methodArn", "*")

# #     if api_key not in VALID_KEYS:
# #         return {
# #             "principalId": "unauthorized",
# #             "policyDocument": {
# #                 "Version": "2012-10-17",
# #                 "Statement": [
# #                     {
# #                         "Action": "execute-api:Invoke",
# #                         "Effect": "Deny",
# #                         "Resource": method_arn
# #                     }
# #                 ]
# #             }
# #         }

# #     client_id = VALID_KEYS[api_key]

# #     return {
# #         "principalId": client_id,
# #         "policyDocument": {
# #             "Version": "2012-10-17",
# #             "Statement": [
# #                 {
# #                     "Action": "execute-api:Invoke",
# #                     "Effect": "Allow",
# #                     "Resource": method_arn
# #                 }
# #             ]
# #         },
# #         "context": {
# #             "client_id": client_id
# #         }
# #     }


# import json
# import os
# import boto3
# from boto3.dynamodb.conditions import Index

# dynamodb = boto3.resource(
#     "dynamodb",
#     region_name=os.environ.get("AWS_REGION", "ap-south-1")
# )

# table = dynamodb.Table(
#     os.environ.get("CONFIGS_TABLE", "chatbot_configs")
# )


# def get_client_by_api_key(api_key):
#     # Scan for matching api_key
#     # For production: add a GSI on api_key for O(1) lookup
#     response = table.scan(
#         FilterExpression=boto3.dynamodb.conditions.Attr("api_key").eq(api_key)
#     )
#     items = response.get("Items", [])
#     if items:
#         return items[0]
#     return None


# def handler(event, context):
#     print("AUTHORIZE EVENT:")
#     print(json.dumps(event))

#     headers = event.get("headers") or {}

#     api_key = (
#         headers.get("x-api-key")
#         or headers.get("X-Api-Key")
#         or headers.get("X-API-Key")
#     )

#     method_arn = event.get("methodArn", "*")

#     if not api_key:
#         return deny("no-key", method_arn)

#     # Lookup in DynamoDB
#     client = get_client_by_api_key(api_key)

#     if not client or not client.get("active"):
#         return deny("unauthorized", method_arn)

#     client_id = client["client_id"]
#     print(f"Authorized: {client_id}")

#     return {
#         "principalId": client_id,
#         "policyDocument": {
#             "Version": "2012-10-17",
#             "Statement": [{
#                 "Action":   "execute-api:Invoke",
#                 "Effect":   "Allow",
#                 "Resource": method_arn
#             }]
#         },
#         "context": {
#             "client_id": client_id
#         }
#     }


# def deny(principal, method_arn):
#     return {
#         "principalId": principal,
#         "policyDocument": {
#             "Version": "2012-10-17",
#             "Statement": [{
#                 "Action":   "execute-api:Invoke",
#                 "Effect":   "Deny",
#                 "Resource": method_arn
#             }]
#         }
#     }
import json
import os
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ.get("AWS_REGION", "ap-south-1")
)

table = dynamodb.Table(
    os.environ.get("CONFIGS_TABLE", "nova-chatbot-configs")
)


def get_client_by_api_key(api_key):
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr("api_key").eq(api_key)
    )
    items = response.get("Items", [])
    if items:
        return items[0]
    return None


def deny(principal, method_arn):
    return {
        "principalId": principal,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action":   "execute-api:Invoke",
                "Effect":   "Deny",
                "Resource": method_arn
            }]
        }
    }


def handler(event, context):
    print("AUTHORIZE EVENT:")
    print(json.dumps(event))

    headers  = event.get("headers") or {}
    api_key  = (
        headers.get("x-api-key")
        or headers.get("X-Api-Key")
        or headers.get("X-API-Key")
    )
    method_arn = event.get("methodArn", "*")

    if not api_key:
        return deny("no-key", method_arn)

    client = get_client_by_api_key(api_key)

    if not client or not client.get("active"):
        return deny("unauthorized", method_arn)

    client_id = client["client_id"]
    print(f"Authorized: {client_id}")

    return {
        "principalId": client_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action":   "execute-api:Invoke",
                "Effect":   "Allow",
                "Resource": method_arn
            }]
        },
        "context": {
            "client_id": client_id
        }
    }