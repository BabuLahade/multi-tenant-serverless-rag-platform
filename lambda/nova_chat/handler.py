# # # import json
# # # from rag import ask

# # # def handler(event, context):
# # #     print("===== FULL API EVENT =====")
# # #     print(json.dumps(event))
# # #     print("==========================")

# # #     raw_body = event.get("body")

# # #     print("===== RAW BODY =====")
# # #     print(repr(raw_body))
# # #     print("====================")
# # #     print("isBase64Encoded =", event.get("isBase64Encoded"))

# # #     if raw_body is None:
# # #         return {
# # #             "statusCode": 400,
# # #             "headers": {
# # #                 "Content-Type": "application/json",
# # #                 "Access-Control-Allow-Origin": "*"
# # #             },
# # #             "body": json.dumps({"error": "Request body is required"})
# # #         }

# # #     if event.get("isBase64Encoded"):
# # #         import base64
# # #         raw_body = base64.b64decode(raw_body).decode("utf-8")

# # #     try:
# # #         # Handling both pre-parsed dicts and raw strings
# # #         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
# # #     except (json.JSONDecodeError, TypeError) as e:
# # #         print(f"===== PARSE ERROR =====\n{str(e)}")
# # #         return {
# # #             "statusCode": 400,
# # #             "headers": {
# # #                 "Content-Type": "application/json",
# # #                 "Access-Control-Allow-Origin": "*"
# # #             },
# # #             "body": json.dumps({"error": "Invalid JSON request body"})
# # #         }

# # #     # Extract client_id from Authorizer context first, fallback to body if running locally/testing
# # #     authorizer_ctx = event.get("requestContext", {}).get("authorizer") or {}
# # #     client_id = authorizer_ctx.get("client_id") or body.get("client_id")
# # #     question = body.get("message")

# # #     if not question or not client_id:
# # #         return {
# # #             "statusCode": 400,
# # #             "headers": {
# # #                 "Content-Type": "application/json",
# # #                 "Access-Control-Allow-Origin": "*"
# # #             },
# # #             "body": json.dumps({"error": "client_id and message are required"})
# # #         }

# # #     result = ask(client_id, question)

# # #     return {
# # #         "statusCode": 200,
# # #         "headers": {
# # #             "Content-Type": "application/json",
# # #             "Access-Control-Allow-Origin": "*"
# # #         },
# # #         "body": json.dumps(result)
# # #     }





# # # # # # # import json

# # # # # # # from rag import ask


# # # # # # # def handler(event, context):

# # # # # # #     body = json.loads(
# # # # # # #         event["body"]
# # # # # # #     )

# # # # # # #     question = body["message"]

# # # # # # #     client_id = body["client_id"]

# # # # # # #     result = ask(
# # # # # # #         client_id,
# # # # # # #         question
# # # # # # #     )

# # # # # # #     return {
# # # # # # #         "statusCode": 200,

# # # # # # #         "headers": {
# # # # # # #             "Content-Type":
# # # # # # #             "application/json"
# # # # # # #         },

# # # # # # #         "body": json.dumps(result)
# # # # # # #     }   
# # # # # # import json

# # # # # # from rag import ask


# # # # # # def handler(event, context):

# # # # # #     # print("===== EVENT =====")
# # # # # #     # print(json.dumps(event))
# # # # # #     # print("=================")

# # # # # #     raw_body = event.get("body")

# # # # # #     if raw_body is None:
# # # # # #         return {
# # # # # #             "statusCode": 400,
# # # # # #             "headers": {
# # # # # #                 "Content-Type": "application/json"
# # # # # #             },
# # # # # #             "body": json.dumps({
# # # # # #                 "error": "Request body is required"
# # # # # #             })
# # # # # #         }

# # # # # #     if event.get("isBase64Encoded"):
# # # # # #         import base64
# # # # # #         raw_body = base64.b64decode(raw_body).decode("utf-8")

# # # # # #     try:
# # # # # #         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
# # # # # #     except (json.JSONDecodeError, TypeError):
# # # # # #         return {
# # # # # #             "statusCode": 400,
# # # # # #             "headers": {
# # # # # #                 "Content-Type": "application/json"
# # # # # #             },
# # # # # #             "body": json.dumps({
# # # # # #                 "error": "Invalid JSON request body"
# # # # # #             })
# # # # # #         }

# # # # # #     question = body.get("message")
# # # # # #     client_id = body.get("client_id")

# # # # # #     if not question or not client_id:
# # # # # #         return {
# # # # # #             "statusCode": 400,
# # # # # #             "headers": {
# # # # # #                 "Content-Type": "application/json"
# # # # # #             },
# # # # # #             "body": json.dumps({
# # # # # #                 "error": "client_id and message are required"
# # # # # #             })
# # # # # #         }

# # # # # #     result = ask(
# # # # # #         client_id,
# # # # # #         question
# # # # # #     )

# # # # # #     return {
# # # # # #         "statusCode": 200,
# # # # # #         "headers": {
# # # # # #             "Content-Type": "application/json"
# # # # # #         },
# # # # # #         "body": json.dumps(result)
# # # # # #     }

# # # # # import json
# # # # # from rag import ask

# # # # # def handler(event, context):
# # # # #     print("===== FULL API EVENT =====")
# # # # #     print(json.dumps(event))
# # # # #     print("==========================")

# # # # #     raw_body = event.get("body")

# # # # #     print("===== RAW BODY =====")
# # # # #     print(repr(raw_body))
# # # # #     print("====================")
# # # # #     print("isBase64Encoded =", event.get("isBase64Encoded"))

# # # # #     if raw_body is None:
# # # # #         return {
# # # # #             "statusCode": 400,
# # # # #             "headers": {"Content-Type": "application/json"},
# # # # #             "body": json.dumps({"error": "Request body is required"})
# # # # #         }

# # # # #     if event.get("isBase64Encoded"):
# # # # #         import base64
# # # # #         raw_body = base64.b64decode(raw_body).decode("utf-8")

# # # # #     try:
# # # # #         # Handling both pre-parsed dicts and raw strings
# # # # #         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
# # # # #     except (json.JSONDecodeError, TypeError) as e:
# # # # #         print(f"===== PARSE ERROR =====\n{str(e)}")
# # # # #         return {
# # # # #             "statusCode": 400,
# # # # #             "headers": {"Content-Type": "application/json"},
# # # # #             "body": json.dumps({"error": "Invalid JSON request body"})
# # # # #         }

# # # # #     question = body.get("message")
# # # # #     client_id = body.get("client_id")

# # # # #     if not question or not client_id:
# # # # #         return {
# # # # #             "statusCode": 400,
# # # # #             "headers": {"Content-Type": "application/json"},
# # # # #             "body": json.dumps({"error": "client_id and message are required"})
# # # # #         }

# # # # #     result = ask(client_id, question)

# # # # #     return {
# # # # #         "statusCode": 200,
# # # # #         "headers": {"Content-Type": "application/json"},
# # # # #         "body": json.dumps(result)
# # # # #     }


# # # # import json
# # # # from rag import ask

# # # # def handler(event, context):
# # # #     print("===== FULL API EVENT =====")
# # # #     print(json.dumps(event))
# # # #     print("==========================")

# # # #     raw_body = event.get("body")

# # # #     print("===== RAW BODY =====")
# # # #     print(repr(raw_body))
# # # #     print("====================")
# # # #     print("isBase64Encoded =", event.get("isBase64Encoded"))

# # # #     if raw_body is None:
# # # #         return {
# # # #             "statusCode": 400,
# # # #             "headers": {
# # # #                 "Content-Type": "application/json",
# # # #                 "Access-Control-Allow-Origin": "*"
# # # #             },
# # # #             "body": json.dumps({"error": "Request body is required"})
# # # #         }

# # # #     if event.get("isBase64Encoded"):
# # # #         import base64
# # # #         raw_body = base64.b64decode(raw_body).decode("utf-8")

# # # #     try:
# # # #         # Handling both pre-parsed dicts and raw strings
# # # #         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
# # # #     except (json.JSONDecodeError, TypeError) as e:
# # # #         print(f"===== PARSE ERROR =====\n{str(e)}")
# # # #         return {
# # # #             "statusCode": 400,
# # # #             "headers": {
# # # #                 "Content-Type": "application/json",
# # # #                 "Access-Control-Allow-Origin": "*"
# # # #             },
# # # #             "body": json.dumps({"error": "Invalid JSON request body"})
# # # #         }

# # # #     question = body.get("message")
# # # #     client_id = body.get("client_id")

# # # #     if not question or not client_id:
# # # #         return {
# # # #             "statusCode": 400,
# # # #             "headers": {
# # # #                 "Content-Type": "application/json",
# # # #                 "Access-Control-Allow-Origin": "*"
# # # #             },
# # # #             "body": json.dumps({"error": "client_id and message are required"})
# # # #         }

# # # #     result = ask(client_id, question)

# # # #     return {
# # # #         "statusCode": 200,
# # # #         "headers": {
# # # #             "Content-Type": "application/json",
# # # #             "Access-Control-Allow-Origin": "*"
# # # #         },
# # # #         "body": json.dumps(result)
# # # #     }


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
# #                     "Effect": "Allow",  # Must be explicitly defined
# #                     "Resource": method_arn
# #                 }
# #             ]
# #         },
# #         "context": {
# #             "client_id": client_id
# #         }
# #     }

# # import json
# # from rag import ask

# # def handler(event, context):
# #     print("===== FULL API EVENT =====")
# #     print(json.dumps(event))
# #     print("==========================")

# #     raw_body = event.get("body")
# #     if raw_body is None:
# #         return {
# #             "statusCode": 400,
# #             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
# #             "body": json.dumps({"error": "Request body is required"})
# #         }

# #     if event.get("isBase64Encoded"):
# #         import base64
# #         raw_body = base64.b64decode(raw_body).decode("utf-8")

# #     try:
# #         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
# #     except (json.JSONDecodeError, TypeError) as e:
# #         return {
# #             "statusCode": 400,
# #             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
# #             "body": json.dumps({"error": "Invalid JSON request body"})
# #         }

# #     # MULTI-TENANT SECURITY LOCK: 
# #     # Extract client_id from Authorizer context first. Fallback to body only if local/testing.
# #     authorizer_ctx = event.get("requestContext", {}).get("authorizer") or {}
# #     client_id = authorizer_ctx.get("client_id") or body.get("client_id")
# #     question = body.get("message")

# #     if not question or not client_id:
# #         return {
# #             "statusCode": 400,
# #             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
# #             "body": json.dumps({"error": "client_id and message are required"})
# #         }

# #     # Query the RAG engine using the securely identified tenant
# #     result = ask(client_id, question)

# #     return {
# #         "statusCode": 200,
# #         "headers": {
# #             "Content-Type": "application/json",
# #             "Access-Control-Allow-Origin": "*"
# #         },
# #         "body": json.dumps(result)
# #     }

# import json
# import traceback
# from rag import ask

# def handler(event, context):
#     print("===== FULL API EVENT =====")
#     print(json.dumps(event))
#     print("==========================")

#     raw_body = event.get("body")
#     if raw_body is None:
#         return {
#             "statusCode": 400,
#             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
#             "body": json.dumps({"error": "Request body is required"})
#         }

#     if event.get("isBase64Encoded"):
#         import base64
#         raw_body = base64.b64decode(raw_body).decode("utf-8")

#     try:
#         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
#     except (json.JSONDecodeError, TypeError) as e:
#         return {
#             "statusCode": 400,
#             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
#             "body": json.dumps({"error": "Invalid JSON request body"})
#         }

#     # MULTI-TENANT SECURITY LOCK: 
#     # Extract client_id strictly from Authorizer context. Do NOT trust the body.
#     authorizer_ctx = event.get("requestContext", {}).get("authorizer", {})
#     client_id = authorizer_ctx.get("client_id")
    
#     if not client_id:
#         return {
#             "statusCode": 403,
#             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
#             "body": json.dumps({"error": "Unauthorized: Tenant identity missing from authorization context."})
#         }

#     question = body.get("message")

#     if not question:
#         return {
#             "statusCode": 400,
#             "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
#             "body": json.dumps({"error": "message is required"})
#         }

#     try:
#         # Query the RAG engine using the securely identified tenant
#         result = ask(client_id, question)
#         return {
#             "statusCode": 200,
#             "headers": {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*"
#             },
#             "body": json.dumps(result)
#         }
#     except Exception as e:
#         print("CRITICAL RAG ERROR:")
#         traceback.print_exc()
#         return {
#             "statusCode": 400,
#             "headers": {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*"
#             },
#             "body": json.dumps({
#                 "error": "Failed to process chat query",
#                 "details": str(e)
#             })
# #         }

# import json
# from rag import ask

# import time

# def log_tenant_metric(client_id: str, metric_name: str, value: float, unit: str = "Count"):
#     """
#     Emits CloudWatch Embedded Metric Format (EMF) directly to stdout.
#     CloudWatch parses this asynchronously with 0ms added latency.
#     """
#     emf_payload = {
#         "_aws": {
#             "Timestamp": int(time.time() * 1000),
#             "CloudWatchMetrics": [
#                 {
#                     "Namespace": "NovaRAG/Tenants",
#                     "Dimensions": [["TenantId"]],
#                     "Metrics": [{"Name": metric_name, "Unit": unit}]
#                 }
#             ]
#         },
#         "TenantId": client_id,
#         metric_name: value
#     }
#     print(json.dumps(emf_payload))

# def handler(event, context):
#     print("===== EVENT =====")
#     print(json.dumps(event))

#     # client_id comes from Lambda Authorizer context only
#     # Never trust client-supplied client_id
#     authorizer_ctx = event.get("requestContext", {}).get("authorizer") or {}
#     client_id = authorizer_ctx.get("client_id")

#     if not client_id:
#         return {
#             "statusCode": 401,
#             "headers": {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*"
#             },
#             "body": json.dumps({"error": "Unauthorized — no client context"})
#         }

#     raw_body = event.get("body")

#     if raw_body is None:
#         return {
#             "statusCode": 400,
#             "headers": {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*"
#             },
#             "body": json.dumps({"error": "Request body is required"})
#         }

#     if event.get("isBase64Encoded"):
#         import base64
#         raw_body = base64.b64decode(raw_body).decode("utf-8")

#     try:
#         body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
#     except (json.JSONDecodeError, TypeError):
#         return {
#             "statusCode": 400,
#             "headers": {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*"
#             },
#             "body": json.dumps({"error": "Invalid JSON request body"})
#         }

#     question = body.get("message", "").strip()

#     if not question:
#         return {
#             "statusCode": 400,
#             "headers": {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*"
#             },
#             "body": json.dumps({"error": "message is required"})
#         }

#     result = ask(client_id, question)

#     return {
#         "statusCode": 200,
#         "headers": {
#             "Content-Type": "application/json",
#             "Access-Control-Allow-Origin": "*"
#         },
#         "body": json.dumps(result)
#     }
# def handler(event, context):
#     start_time = time.time()
    
#     # Extract client_id resolved by the custom authorizer
#     client_id = event.get("requestContext", {}).get("authorizer", {}).get("client_id", "anonymous")
    
#     # 1. Track Invocation per Tenant
#     log_tenant_metric(client_id, "Invocations", 1, "Count")
    
#     try:
#         # ... (Your existing RAG retrieval and LLM call logic) ...
        
#         # Calculate execution latency
#         latency_ms = (time.time() - start_time) * 1000
#         log_tenant_metric(client_id, "LatencyMs", latency_ms, "Milliseconds")
        
#         # Optional: Track approximate token usage if available from your model response
#         # log_tenant_metric(client_id, "TokenUsage", token_count, "Count")
        
#         return response
        
#     except Exception as e:
#         # Track Error per Tenant
#         log_tenant_metric(client_id, "Errors", 1, "Count")
#         raise e

import base64
import json
import time
from rag import ask

def log_tenant_metric(client_id: str, metric_name: str, value: float, unit: str = "Count"):
    """
    Emits CloudWatch Embedded Metric Format (EMF) directly to stdout.
    CloudWatch parses this asynchronously with 0ms added latency.
    """
    emf_payload = {
        "_aws": {
            "Timestamp": int(time.time() * 1000),
            "CloudWatchMetrics": [
                {
                    "Namespace": "NovaRAG/Tenants",
                    "Dimensions": [["TenantId"]],
                    "Metrics": [{"Name": metric_name, "Unit": unit}]
                }
            ]
        },
        "TenantId": client_id,
        metric_name: value
    }
    print(json.dumps(emf_payload))

def handler(event, context):
    start_time = time.time()
    print("===== EVENT =====")
    print(json.dumps(event))

    # client_id comes from Lambda Authorizer context only
    authorizer_ctx = event.get("requestContext", {}).get("authorizer") or {}
    client_id = authorizer_ctx.get("client_id")

    if not client_id:
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Unauthorized — no client context"})
        }

    # 1. Track invocation metric per tenant
    log_tenant_metric(client_id, "Invocations", 1, "Count")

    raw_body = event.get("body")

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
        raw_body = base64.b64decode(raw_body).decode("utf-8")

    try:
        body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Invalid JSON request body"})
        }

    question = body.get("message", "").strip()

    if not question:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "message is required"})
        }

    try:
        # Execute RAG query against tenant-partitioned vectors
        result = ask(client_id, question)

        # 2. Track execution latency per tenant
        latency_ms = (time.time() - start_time) * 1000
        log_tenant_metric(client_id, "LatencyMs", latency_ms, "Milliseconds")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        # 3. Track errors per tenant
        log_tenant_metric(client_id, "Errors", 1, "Count")
        
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return {
                "statusCode": 429,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "AI provider rate limit exceeded. Please wait 60 seconds and try again."})
            }
            
        raise e