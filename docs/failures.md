# FAILURES.md

Real incidents encountered while building Nova RAG Platform.

---

## 2026-01 — Lambda returned 500 on all API Gateway requests

**Symptom:** POST /chat returned 500. Direct Lambda invoke worked fine.

**Root cause:** `json.loads(event["body"])` crashed when body was None.
API Gateway passes None when Content-Type header is missing.

**Fix:** Added safe body parsing with None check and try/except before json.loads.

**Prevention:** Always use `event.get("body") or "{}"` pattern in Lambda handlers.

---

## 2026-01 — Embeddings failing silently on new content

**Symptom:** nova-ingest ran successfully but DynamoDB had no new chunks.

**Root cause:** EMBED_MODEL was set to "gemini-embedding-2" which does not exist.
API returned 404 but code swallowed the error.

**Fix:** Changed model to "gemini-embedding-001". Added explicit error logging.

**Prevention:** Always validate model names against API docs before deploying.

---

## 2026-01 — Widget showing "Unable to reach server" from localhost

**Symptom:** Chat widget worked when Lambda was invoked directly.
Failed with network error when called from browser.

**Root cause:** CORS policy blocked browser requests from localhost:8080
to execute-api.ap-south-1.amazonaws.com.

**Fix:** Added Access-Control-Allow-Origin: * headers to all Lambda responses.
Added OPTIONS method to API Gateway for preflight requests.

**Prevention:** Always add CORS headers from day one on any browser-facing API.

---

## 2026-01 — Wrong AWS region causing ResourceNotFoundException

**Symptom:** Lambda logs showed ResourceNotFoundException for DynamoDB table.

**Root cause:** Region hardcoded as "ap-south-1" in some files, "eu-north-1" in others.
Table existed in ap-south-1 but some clients connected to eu-north-1.

**Fix:** Replaced all hardcoded regions with os.environ.get("AWS_REGION", "ap-south-1").

**Prevention:** Never hardcode AWS region. Always read from environment variables.

---

## 2026-01 — S3 event not triggering SQS

**Symptom:** Files uploaded to S3 but nova-ingest Lambda never triggered.

**Root cause:** SQS queue policy did not allow S3 to send messages.
S3 event notification was configured but messages were silently dropped.

**Fix:** Added aws_sqs_queue_policy resource in Terraform granting S3 permission.

**Prevention:** Always test the full pipeline end-to-end after adding event sources.