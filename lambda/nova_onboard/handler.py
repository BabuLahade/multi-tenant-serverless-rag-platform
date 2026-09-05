import json
import os
import uuid
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ.get("AWS_REGION", "ap-south-1")
)

configs_table = dynamodb.Table(
    os.environ.get("CONFIGS_TABLE", "chatbot_configs")
)
apigateway = boto3.client(
    "apigateway",
    region_name=os.environ.get("AWS_REGION", "ap-south-1")
)

USAGE_PLAN_ID = os.environ.get("USAGE_PLAN_ID", "")

API_GATEWAY_URL = os.environ.get(
    "API_GATEWAY_URL",
    "https://dh90wd8pxc.execute-api.ap-south-1.amazonaws.com/dev"
)

WIDGET_URL = os.environ.get(
    "WIDGET_URL",
    "https://yourdomain.com/widget.js"
)


def generate_api_key(client_id):
    unique = str(uuid.uuid4()).replace("-", "")[:24]
    return f"nova_{client_id}_{unique}"


def handler(event, context):
    print(json.dumps(event))

    raw_body = event.get("body") or "{}"

    if event.get("isBase64Encoded"):
        import base64
        raw_body = base64.b64decode(raw_body).decode("utf-8")

    try:
        body = raw_body if isinstance(raw_body, dict) else json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return respond(400, {"error": "Invalid JSON"})

    # Required fields
    client_id   = body.get("client_id", "").strip().lower()
    site_url    = body.get("site_url", "").strip()
    bot_name    = body.get("bot_name", "Nova AI").strip()
    brand_color = body.get("brand_color", "#2563eb").strip()
    system_prompt = body.get(
        "system_prompt",
        f"You are a helpful assistant for {bot_name}."
    ).strip()

    if not client_id or not site_url:
        return respond(400, {"error": "client_id and site_url are required"})

    # Check if client already exists
    existing = configs_table.get_item(
        Key={"client_id": client_id}
    ).get("Item")

    if existing:
        return respond(409, {
            "error": f"Client '{client_id}' already exists. Use a different client_id."
        })

    # Generate unique API key
    api_key = generate_api_key(client_id)

    # Save to DynamoDB
    configs_table.put_item(Item={
        "client_id":     client_id,
        "api_key":       api_key,
        "site_url":      site_url,
        "bot_name":      bot_name,
        "brand_color":   brand_color,
        "system_prompt": system_prompt,
        "active":        True
    })

    print(f"Created client: {client_id} with key: {api_key}")

    if USAGE_PLAN_ID:
        try:
            # 1. Create the API Key in AWS
            api_key_response = apigateway.create_api_key(
                name=f"nova-tenant-{client_id}",
                value=api_key,
                enabled=True
            )
            key_id = api_key_response['id']
            print(f"API Key registered in API Gateway with ID: {key_id}")

            # 2. Attach the Key to the Usage Plan
            apigateway.create_usage_plan_key(
                usagePlanId=USAGE_PLAN_ID,
                keyId=key_id,
                keyType='API_KEY'
            )
            print(f"API Key attached to Usage Plan: {USAGE_PLAN_ID}")
            
        except Exception as e:
            print(f"Failed to register key with API Gateway: {e}")
            # Depending on strictness, you could return a 500 error here
    else:
        print("WARNING: USAGE_PLAN_ID env var not set. Skipping API Gateway registration.")
    # ==========================================
    # Trigger crawl automatically
    try:
        sqs = boto3.client(
            "sqs",
            region_name=os.environ.get("AWS_REGION", "ap-south-1")
        )
        sqs.send_message(
            QueueUrl=os.environ.get("SQS_QUEUE_URL"),
            MessageBody=json.dumps({
                "client_id": client_id,
                "url":       site_url
            })
        )
        print(f"Crawl queued for {site_url}")
        crawl_status = "queued"
    except Exception as e:
        print(f"Crawl queue failed: {e}")
        crawl_status = "failed — trigger manually via POST /crawl"

    # Build the script snippet
    snippet = (
        f'<script\n'
        f'  src="{WIDGET_URL}"\n'
        f'  data-api-key="{api_key}"\n'
        f'  data-bot-name="{bot_name}"\n'
        f'  data-brand-color="{brand_color}"\n'
        f'></script>'
    )

    return respond(200, {
        "client_id":   client_id,
        "api_key":     api_key,
        "bot_name":    bot_name,
        "crawl":       crawl_status,
        "snippet":     snippet,
        "message":     f"Client '{client_id}' created. Paste the snippet on your website."
    })


def respond(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type":                "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }