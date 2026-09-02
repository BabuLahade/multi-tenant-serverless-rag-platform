# # # import json

# # # from rag import ask


# # # def handler(event, context):

# # #     body = json.loads(
# # #         event["body"]
# # #     )

# # #     question = body["message"]

# # #     client_id = body["client_id"]

# # #     result = ask(
# # #         client_id,
# # #         question
# # #     )

# # #     return {
# # #         "statusCode": 200,

# # #         "headers": {
# # #             "Content-Type":
# # #             "application/json"
# # #         },

# # #         "body": json.dumps(result)
# # #     }   
# # import json

# # from rag import ask


# # def handler(event, context):

# #     # print("===== EVENT =====")
# #     # print(json.dumps(event))
# #     # print("=================")

# #     raw_body = event.get("body")

# #     if raw_body is None:
# #         return {
# #             "statusCode": 400,
# #             "headers": {
# #                 "Content-Type": "application/json"
# #             },
# #             "body": json.dumps({
# #                 "error": "Request body is required"
# #             })
# #         }

# #     if event.get("isBase64Encoded"):
# #         import base64
# #         raw_body = base64.b64decode(raw_body).decode("utf-8")

# #     try:
# #         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
# #     except (json.JSONDecodeError, TypeError):
# #         return {
# #             "statusCode": 400,
# #             "headers": {
# #                 "Content-Type": "application/json"
# #             },
# #             "body": json.dumps({
# #                 "error": "Invalid JSON request body"
# #             })
# #         }

# #     question = body.get("message")
# #     client_id = body.get("client_id")

# #     if not question or not client_id:
# #         return {
# #             "statusCode": 400,
# #             "headers": {
# #                 "Content-Type": "application/json"
# #             },
# #             "body": json.dumps({
# #                 "error": "client_id and message are required"
# #             })
# #         }

# #     result = ask(
# #         client_id,
# #         question
# #     )

# #     return {
# #         "statusCode": 200,
# #         "headers": {
# #             "Content-Type": "application/json"
# #         },
# #         "body": json.dumps(result)
# #     }

# import json
# from rag import ask

# def handler(event, context):
#     print("===== FULL API EVENT =====")
#     print(json.dumps(event))
#     print("==========================")

#     raw_body = event.get("body")

#     print("===== RAW BODY =====")
#     print(repr(raw_body))
#     print("====================")
#     print("isBase64Encoded =", event.get("isBase64Encoded"))

#     if raw_body is None:
#         return {
#             "statusCode": 400,
#             "headers": {"Content-Type": "application/json"},
#             "body": json.dumps({"error": "Request body is required"})
#         }

#     if event.get("isBase64Encoded"):
#         import base64
#         raw_body = base64.b64decode(raw_body).decode("utf-8")

#     try:
#         # Handling both pre-parsed dicts and raw strings
#         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
#     except (json.JSONDecodeError, TypeError) as e:
#         print(f"===== PARSE ERROR =====\n{str(e)}")
#         return {
#             "statusCode": 400,
#             "headers": {"Content-Type": "application/json"},
#             "body": json.dumps({"error": "Invalid JSON request body"})
#         }

#     question = body.get("message")
#     client_id = body.get("client_id")

#     if not question or not client_id:
#         return {
#             "statusCode": 400,
#             "headers": {"Content-Type": "application/json"},
#             "body": json.dumps({"error": "client_id and message are required"})
#         }

#     result = ask(client_id, question)

#     return {
#         "statusCode": 200,
#         "headers": {"Content-Type": "application/json"},
#         "body": json.dumps(result)
#     }


import json
from rag import ask

def handler(event, context):
    print("===== FULL API EVENT =====")
    print(json.dumps(event))
    print("==========================")

    raw_body = event.get("body")

    print("===== RAW BODY =====")
    print(repr(raw_body))
    print("====================")
    print("isBase64Encoded =", event.get("isBase64Encoded"))

    if raw_body is None:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Request body is required"})
        }

    if event.get("isBase64Encoded"):
        import base64
        raw_body = base64.b64decode(raw_body).decode("utf-8")

    try:
        # Handling both pre-parsed dicts and raw strings
        body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"===== PARSE ERROR =====\n{str(e)}")
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Invalid JSON request body"})
        }

    question = body.get("message")
    client_id = body.get("client_id")

    if not question or not client_id:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "client_id and message are required"})
        }

    result = ask(client_id, question)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }