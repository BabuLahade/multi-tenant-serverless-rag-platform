# FAILURES.md
# Failure & Troubleshooting Log — Nova AI Platform

**Project:** `multi-tenant-serverless-rag-platform` / Nova AI Platform  
**Region:** `ap-south-1`  
**Current status:** Core crawl → SQS → ingest → DynamoDB and chat → RAG flows are working.

---

## 1. Purpose

This document records the major failures, symptoms, root causes, fixes, verification steps, and lessons learned during development and deployment.

It is an engineering postmortem, not simply an error list.

---

## 2. Architecture Context

Main components:

- AWS Lambda: `nova-crawl`, `nova-ingest`, `nova-chat`, `nova-authorizer`
- API Gateway REST API
- DynamoDB
- S3
- SQS / DLQ
- EventBridge
- CloudWatch
- X-Ray
- Secrets Manager
- Terraform
- Gemini API
- Python
- Frontend/widget

Core flow:

```text
Browser
   |
   v
API Gateway
   |
   +-- /crawl --> nova-crawl --> SQS --> nova-ingest --> DynamoDB
   |
   +-- /chat --> nova-chat --> DynamoDB --> RAG --> Gemini
```

Authentication:

```text
x-api-key
   |
   v
API Gateway
   |
   v
Lambda REQUEST Authorizer
   |
   +-- valid --> Allow
   +-- invalid --> Deny
```

---

# 3. AWS Account Migration

## Symptom

The original AWS account became unavailable because it was suspended/closed. Existing infrastructure could no longer be treated as usable.

## Root Cause

The original AWS account was no longer usable for this project.

## Fix

A new AWS account was created and the infrastructure was recreated/migrated.

Current account used during recovery:

```text
169748358276
```

Region:

```text
ap-south-1
```

## Verification

Terraform deployment succeeded in the new account and a new API Gateway was created.

## Lesson

Always verify AWS identity before debugging:

```powershell
aws sts get-caller-identity
```

A resource failure can actually be an account/profile/region mismatch.

---

# 4. AWS CLI / Account Mismatch Risk

## Symptom

Old resource identifiers and new infrastructure became mixed during migration.

## Root Cause

AWS resource IDs belong to particular accounts/regions/environments. Old IDs cannot simply be reused after migration.

## Fix

Verify:

```powershell
aws sts get-caller-identity
aws configure list
aws configure get region
```

## Lesson

Debug in this order:

```text
Account -> Region -> Resource ID -> Resource state
```

---

# 5. S3 Global Bucket Name Conflict

## Symptom

The intended bucket:

```text
nova-raw-content
```

could not be used.

## Root Cause

S3 bucket names are globally unique. A name may already be unavailable even if it is not visible in the current AWS account.

## Fix

Use a globally unique name, for example:

```text
nova-raw-content-<unique-suffix>
```

## Lesson

Never assume a generic S3 name is available in a new AWS account.

---

# 6. Terraform S3/SQS Dependency Cycle

## Symptom

Terraform reported a dependency cycle involving the S3 bucket, SQS queue, queue policy, and notification configuration.

## Root Cause

The module wiring caused S3 and SQS modules to depend on each other's outputs.

Conceptually:

```text
S3 -> SQS
SQS -> S3
```

which creates:

```text
A -> B -> A
```

## Fix

The dependency direction was redesigned so the bucket exists independently and the queue policy/notification consumes the required bucket and queue information.

Preferred relationship:

```text
S3 bucket
   |
   v
SQS queue policy
   |
   v
S3 notification
```

## Lesson

Terraform modules must form a directed dependency graph. Avoid circular module outputs.

---

# 7. S3 → SQS Notification Validation Failure

## Symptom

S3 notification configuration failed with:

```text
Unable to validate the following destination configurations
```

## Investigation

Checked:

- SQS queue ARN
- S3 bucket ARN
- SQS queue policy
- `aws:SourceArn`
- `aws:SourceAccount`
- Terraform resource ordering
- encryption/KMS considerations

## Root Cause

S3 could not validate the SQS destination because the destination/policy/deployment ordering was not correct.

The queue policy needs to permit:

```text
Principal: s3.amazonaws.com
Action: SQS:SendMessage
Resource: <queue ARN>
```

with source restrictions based on the actual bucket.

## Fix

Corrected the queue policy and ensured it existed before S3 notification validation.

## Lesson

For S3 → SQS always validate:

```text
Bucket ARN
   ↓
Queue ARN
   ↓
Queue policy
   ↓
SourceArn
   ↓
SourceAccount
   ↓
Notification
```

If a customer-managed KMS key is used, KMS permissions must also be considered.

---

# 8. `nova-ingest` ReceiveMessage AccessDenied

## Symptom

The ingest Lambda failed with an authorization error involving:

```text
sqs:ReceiveMessage
```

## Root Cause

The Lambda execution role lacked the SQS permissions required to consume messages.

## Fix

Added permissions including:

```text
sqs:ReceiveMessage
sqs:DeleteMessage
sqs:GetQueueAttributes
```

for the ingest queue ARN.

## Verification

CloudWatch later showed successful SQS event reception and processing.

## Lesson

Distinguish these two permission paths:

```text
S3 -> SQS
```

and:

```text
SQS -> Lambda
```

They require different authorization configuration.

---

# 9. Wrong API Gateway ID After Migration

## Symptom

The frontend produced:

```text
Invalid API identifier specified
```

The old API ID was:

```text
f9bdmtcslf
```

The new API ID was:

```text
dh90wd8pxc
```

## Root Cause

The frontend still referenced the old API Gateway endpoint.

## Fix

Updated the frontend to:

```text
https://dh90wd8pxc.execute-api.ap-south-1.amazonaws.com/dev
```

## Lesson

After infrastructure recreation, search the repository for stale IDs.

Example:

```powershell
Get-ChildItem -Recurse -File | Select-String "f9bdmtcslf"
```

---

# 10. API Gateway OPTIONS 403 / MissingAuthenticationToken

## Symptom

Browser CORS preflight:

```text
OPTIONS /chat
```

returned:

```text
403 MissingAuthenticationTokenException
```

This was confusing because API Gateway showed:

```text
authorizationType: NONE
```

for OPTIONS.

## Investigation

The OPTIONS method existed and used a MOCK integration.

The problem was not the method definition itself.

The `dev` stage was pointing to an older API Gateway deployment snapshot.

Therefore:

```text
Current REST API configuration
        !=
Stage deployment snapshot
```

## Root Cause

The stage had not been redeployed after API Gateway method/integration changes.

## Fix

Manual deployment:

```powershell
aws apigateway create-deployment `
  --rest-api-id dh90wd8pxc `
  --stage-name dev `
  --description "Phase 8.2 CORS deployment fix" `
  --region ap-south-1
```

Deployment created:

```text
knk1sf
```

## Verification

OPTIONS changed from:

```text
403
```

to:

```text
200
```

with CORS headers.

## Lesson

For REST API Gateway:

```text
Modify method/integration
        ↓
Create deployment
        ↓
Stage points to deployment
```

A current method definition does not automatically mean the stage serves it.

---

# 11. Terraform API Gateway Deployment Had No Trigger

## Symptom

Terraform could update API Gateway resources without necessarily forcing a new deployment snapshot.

## Root Cause

The deployment resource had `depends_on`, but no explicit configuration-change trigger.

Existing pattern:

```hcl
resource "aws_api_gateway_deployment" "rag" {
  depends_on = [
    aws_api_gateway_integration.chat,
    aws_api_gateway_integration.crawl,
    aws_api_gateway_integration.chat_options,
    aws_api_gateway_integration.crawl_options
  ]

  rest_api_id = aws_api_gateway_rest_api.rag_api.id
}
```

## Why This Matters

`depends_on` controls ordering.

It does not automatically mean:

```text
configuration changed -> new deployment
```

## Follow-up

Add a robust deployment trigger hash over relevant API Gateway resources, for example:

```hcl
triggers = {
  redeployment = sha1(jsonencode([
    aws_api_gateway_resource.chat.id,
    aws_api_gateway_method.chat.id,
    aws_api_gateway_integration.chat.id,
    aws_api_gateway_resource.crawl.id,
    aws_api_gateway_method.crawl.id,
    aws_api_gateway_integration.crawl.id
  ]))
}
```

The final trigger should include every configuration change that must invalidate the deployment.

## Lesson

Terraform dependency ordering and API deployment invalidation are separate concerns.

---

# 12. CORS Preflight Recovery

## Before

```text
OPTIONS /chat -> 403
```

## After

```text
OPTIONS /chat -> 200
```

Expected headers included:

```text
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: OPTIONS,POST
```

## Conclusion

The CORS method configuration was substantially correct. The active stage was stale.

---

# 13. Chat API 401 Unauthorized

## Symptom

The browser received:

```text
401 Unauthorized
```

## Root Cause

`/chat` uses a CUSTOM REQUEST authorizer whose identity source is:

```text
method.request.header.x-api-key
```

The frontend initially did not send the required header.

## Fix

Added:

```http
x-api-key: fintech-key
```

for the demo tenant.

## Verification

The authenticated request reached the chat Lambda and returned a valid RAG response.

## Lesson

For a custom API Gateway authorizer verify:

```text
Client header
   ↓
API Gateway identity source
   ↓
Authorizer
   ↓
Allow/Deny
   ↓
Backend
```

---

# 14. Authorizer Response Format Issue

## Background

The authorizer implementation evolved from an `isAuthorized`-style response to the IAM policy response required by the current REST API REQUEST authorizer.

Current intended successful response:

```json
{
  "principalId": "fintech",
  "policyDocument": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "execute-api:Invoke",
        "Effect": "Allow",
        "Resource": "..."
      }
    ]
  },
  "context": {
    "client_id": "fintech"
  }
}
```

## Important Code Issue

The local authorizer source at one point had the Allow statement without:

```json
"Effect": "Allow"
```

The deployed behavior nevertheless authorized the tested request, so local source and deployed Lambda should not be assumed identical without verification.

## Required Follow-up

Confirm the deployed authorizer explicitly returns:

```json
"Effect": "Allow"
```

for valid credentials.

## Lesson

Do not mix authorizer response formats between API Gateway REST APIs and HTTP APIs.

---

# 15. PowerShell Invalid JSON 400

## Symptom

Chat returned:

```json
{
  "error": "Invalid JSON request body"
}
```

## Root Cause

The request body arriving at Lambda was not valid JSON after shell/curl argument handling.

Lambda was correctly rejecting it at:

```python
json.loads(raw_body)
```

## Fix

Use PowerShell JSON serialization:

```powershell
$chat_body = @{
    client_id = "fintech"
    message   = "What is the purpose of example.com according to the documentation?"
} | ConvertTo-Json -Compress
```

Then:

```powershell
Invoke-RestMethod -Uri "https://dh90wd8pxc.execute-api.ap-south-1.amazonaws.com/dev/chat" `
    -Method POST `
    -Headers @{
        "Content-Type" = "application/json"
        "x-api-key"    = "fintech-key"
    } `
    -Body $chat_body
```

## Verification

The API returned:

```text
answer: The purpose of example.com is for use in documentation examples without needing permission.
sources: 2
grounded: True
```

## Lesson

For PowerShell API testing, prefer:

```text
ConvertTo-Json -Compress
+
Invoke-RestMethod
```

---

# 16. Frontend API Authentication Configuration

## Symptom

The frontend loaded but API requests were unauthorized.

## Root Cause

The frontend JavaScript did not initially send the API key.

## Fix

The request was updated to include:

```javascript
headers: {
  "Content-Type": "application/json",
  "x-api-key": "fintech-key"
}
```

## Lesson

A healthy frontend does not imply a healthy API request.

Use browser Network inspection to verify:

- URL
- method
- request headers
- request body
- status code
- response body

---

# 17. Chrome DevTools `.well-known` 404

## Symptom

The local Python server logged:

```text
GET /.well-known/appspecific/com.chrome.devtools.json
```

with:

```text
404
```

## Root Cause

This is a Chrome DevTools/browser probe.

It is not an application route required by Nova AI Platform.

## Verification

Actual application resources returned successfully:

```text
index.html -> 200
app.js     -> 200/304
style.css  -> 200/304
```

## Classification

```text
NON-ISSUE
```

## Lesson

Not every browser-generated 404 is an application problem.

---

# 18. End-to-End Chat RAG Verification

The system was tested layer by layer.

```text
Frontend
   ↓
API Gateway
   ↓
Authorizer
   ↓
Chat Lambda
   ↓
DynamoDB retrieval
   ↓
RAG
   ↓
Gemini
   ↓
Response
```

Final verified response:

```text
answer:
The purpose of example.com is for use in documentation examples without needing permission.

sources: 2
grounded: True
```

## Conclusion

The core chat RAG flow is operational.

---

# 19. End-to-End Crawl / Ingest Verification

The crawl API was invoked with:

```json
{
  "client_id": "fintech",
  "url": "https://example.com"
}
```

CloudWatch logs showed:

```text
SQS event received
```

then:

```text
Ingesting URL: https://example.com for client: fintech
```

then:

```text
Total chunks: 1
```

then:

```text
Saved fintech:chunk_0
```

then:

```text
Successfully processed 1 chunks from https://example.com
```

SQS queue:

```text
nova-ingest-queue
```

X-Ray trace information was also visible.

## Conclusion

This pipeline is working:

```text
API Gateway
   ↓
nova-crawl
   ↓
SQS
   ↓
nova-ingest
   ↓
DynamoDB
```

---

# 20. Duplicate Crawl / Idempotency Observation

## Observation

The same crawl was invoked more than once.

The generated key remained:

```text
fintech:chunk_0
```

## Interpretation

The deterministic key prevents uncontrolled creation of a differently named chunk for the same source/index, but this should be explicitly designed and verified as an idempotency mechanism.

## Production Requirement

Define an explicit strategy using one or more of:

- deterministic document/chunk IDs
- content hashes
- source URL + chunk index
- version IDs
- conditional writes
- document versioning/deletion

## Lesson

SQS and event-driven processing must assume retries and duplicate delivery.

---

# 21. Security Finding: Request Body `client_id` Is Trusted

## Current Risk

The chat Lambda currently accepts a body such as:

```json
{
  "client_id": "fintech",
  "message": "..."
}
```

and uses that client ID for RAG.

This creates a tenant-isolation risk because the request body is user-controlled.

## Correct Security Model

Tenant identity should come from API Gateway authorizer context:

```python
authorizer = (
    event.get("requestContext", {})
         .get("authorizer", {})
)

client_id = authorizer.get("client_id")
```

The backend should ignore a user-supplied tenant ID as an authority.

## Recommended Request

Client sends:

```json
{
  "message": "..."
}
```

Authentication supplies:

```text
x-api-key
    ↓
authorizer
    ↓
client_id
```

Backend uses:

```text
authorizer.client_id
```

## Status

**Not yet fully hardened.**

Do not claim tenant isolation is completely fixed until this change and its tests are complete.

---

# 22. Tenant Isolation Test

## Test Already Performed

Used:

```text
x-api-key: healthcare-key
```

with:

```text
client_id: fintech
```

and a KYC question.

Result:

```text
sources: 0
grounded: True
```

## Why It Is Not Definitive

There was no known fintech KYC document to prove that the request had been blocked from fintech data.

## Required Definitive Test

Use a known fintech-only question:

```text
x-api-key: healthcare-key
body client_id: fintech
question: What is the purpose of example.com according to the documentation?
```

Expected:

```text
Must NOT return the known fintech answer.
```

Repeat with:

```text
x-api-key: store-key
body client_id: fintech
```

Expected:

```text
Must NOT retrieve fintech data.
```

Then change the backend to use authorizer context and repeat the tests.

---

# 23. Frontend Hardcoded API Key

## Current State

The demo frontend contains a tenant API key.

This is acceptable for:

```text
local development
demo
prototype
```

but not as a production secret.

## Risk

Browser JavaScript is inspectable.

Therefore a permanent privileged secret cannot be treated as confidential when embedded in a public frontend.

## Production Direction

Consider:

- short-lived tokens
- signed sessions
- backend-for-frontend
- controlled public API credentials
- tenant-specific public identifiers
- server-side secret storage
- rate limiting

## Lesson

Never put a real privileged secret in a public frontend bundle.

---

# 24. Manual API Gateway Deployment Drift

## Symptom

A manual CLI deployment was required to make the current API configuration active.

Deployment:

```text
knk1sf
```

## Risk

Manual changes can create drift between:

```text
Terraform state
```

and:

```text
actual AWS state
```

## Lesson

Manual deployment is useful for diagnosis/recovery. The final production implementation should be reproducible entirely through Terraform.

---

# 25. 500/502 Troubleshooting Boundary

For any future API Gateway 500/502, investigate:

```text
Client
   ↓
API Gateway
   ↓
Integration
   ↓
Lambda invoke permission
   ↓
Lambda execution
   ↓
Lambda exception
```

Check:

- API Gateway execution/access logs
- Lambda CloudWatch logs
- X-Ray traces
- Lambda configuration
- Lambda invoke permissions
- integration configuration

Do not label a 500/502 as an AWS problem without locating the failing layer.

Historical 500/502 causes should only be called confirmed when corresponding logs/evidence exist.

---

# 26. Root Cause vs Symptom

| Symptom | Root Cause |
|---|---|
| Invalid API identifier | Frontend referenced old API Gateway ID |
| OPTIONS 403 | Stage used stale API Gateway deployment |
| OPTIONS showed NONE but failed | Current REST API config differed from deployed snapshot |
| S3 notification validation failure | S3 could not validate authorized SQS destination |
| Terraform dependency cycle | S3/SQS modules depended on each other's outputs |
| ReceiveMessage AccessDenied | Lambda role lacked SQS permissions |
| Chat 401 | Missing `x-api-key` |
| Invalid JSON 400 | PowerShell request body construction |
| Chrome `.well-known` 404 | Browser DevTools probe |
| Potential cross-tenant access | Backend trusts body `client_id` |
| Duplicate crawl observation | Idempotency strategy needs explicit design |

---

# 27. Current Working Baseline

Verified:

### API Gateway

```text
API ID: dh90wd8pxc
Stage: dev
Region: ap-south-1
```

### Chat

```text
POST /dev/chat
```

with:

```text
Content-Type: application/json
x-api-key: fintech-key
```

Returned:

```text
sources: 2
grounded: True
```

### Crawl

```text
POST /dev/crawl
```

works.

### SQS

```text
nova-ingest-queue
```

receives crawl events.

### Ingest

CloudWatch confirmed successful processing.

### DynamoDB

Tenant-qualified chunk:

```text
fintech:chunk_0
```

was saved.

### X-Ray

Trace IDs were visible during Lambda execution.

### Frontend

Local server:

```text
http://localhost:8080
```

successfully served:

```text
index.html
app.js
style.css
```

---

# 28. Recovery Checklist

When the platform breaks, do not immediately change Terraform.

## Step 1 — Verify account

```powershell
aws sts get-caller-identity
```

## Step 2 — Verify region

```powershell
aws configure get region
```

Expected:

```text
ap-south-1
```

## Step 3 — Verify API

```powershell
aws apigateway get-rest-api `
  --rest-api-id dh90wd8pxc `
  --region ap-south-1
```

## Step 4 — Test CORS

```powershell
curl.exe -i -X OPTIONS `
  "https://dh90wd8pxc.execute-api.ap-south-1.amazonaws.com/dev/chat" `
  -H "Origin: http://localhost:8080" `
  -H "Access-Control-Request-Method: POST" `
  -H "Access-Control-Request-Headers: content-type,x-api-key"
```

Expected:

```text
HTTP 200
```

## Step 5 — Test authorizer

Confirm `x-api-key` is present.

## Step 6 — Test valid JSON

Use:

```powershell
ConvertTo-Json -Compress
```

and:

```powershell
Invoke-RestMethod
```

## Step 7 — Inspect Lambda logs

Check:

```text
nova-authorizer
nova-chat
nova-crawl
nova-ingest
```

## Step 8 — Inspect SQS

Confirm messages are received/deleted.

## Step 9 — Inspect DynamoDB

Confirm expected tenant records.

## Step 10 — Inspect X-Ray

Locate latency/failure boundaries.

---

# 29. Prevention Rules

## Infrastructure

- Terraform is the source of truth.
- Avoid manual production changes.
- Add API Gateway deployment triggers.
- Avoid module dependency cycles.
- Use globally unique S3 names.
- Explicitly manage Lambda dependencies.

## Security

- Never trust request-body tenant IDs.
- Derive tenant identity from authenticated context.
- Do not expose real secrets in frontend code.
- Scope IAM permissions to specific resources.
- Use least privilege.
- Keep Secrets Manager values out of source control.

## Reliability

- Design ingestion for idempotency.
- Expect SQS retries.
- Configure and monitor DLQs.
- Monitor queue age.
- Monitor Lambda errors/throttles.
- Monitor API P99 latency.
- Add CloudWatch alarms.

## Debugging

Separate:

```text
Browser
API Gateway
Authorizer
Lambda
SQS
DynamoDB
RAG/Gemini
```

Do not debug every layer simultaneously.

---

# 30. Production Hardening Still Required

## High Priority

- [ ] Derive `client_id` from authorizer context in chat.
- [ ] Apply the same tenant-authentication model to crawl.
- [ ] Perform definitive cross-tenant tests.
- [ ] Add API Gateway deployment triggers.
- [ ] Remove manual deployment drift.
- [ ] Confirm deployed authorizer returns explicit `Effect: Allow`.
- [ ] Establish a production-safe credential strategy.

## Reliability

- [ ] Explicit ingestion idempotency.
- [ ] DLQ monitoring.
- [ ] Queue-age alarms.
- [ ] Lambda error/throttle alarms.
- [ ] Chat error-rate alarms.
- [ ] API P99 latency monitoring.

## Observability

- [ ] CloudWatch dashboard.
- [ ] Structured logging.
- [ ] Request/correlation IDs.
- [ ] X-Ray tracing.
- [ ] Custom metrics.

---

# 31. Engineering Lessons Learned

### 1. Verify AWS identity first

A wrong account or region can make correct infrastructure look broken.

### 2. API Gateway configuration is not the same as deployment state

A method can exist in the REST API while the stage serves an older deployment.

### 3. `depends_on` is not a deployment trigger

Terraform ordering and API Gateway deployment invalidation are separate problems.

### 4. AWS authorization is layered

Examples:

```text
S3 -> SQS
Lambda -> SQS
API Gateway -> Lambda
API Gateway -> Authorizer
```

Each path can fail independently.

### 5. Browser testing is insufficient

Direct API tests plus CloudWatch logs are essential for isolation.

### 6. Tenant identity is a security boundary

A tenant ID supplied by the browser is not authentication.

### 7. Event-driven systems must tolerate retries

Duplicate messages are normal. Idempotency must be designed.

### 8. Manual fixes should become infrastructure code

A CLI fix can prove a diagnosis, but Terraform should encode the final solution.

---

# 32. Incident Timeline

```text
AWS account became unavailable
        ↓
Migrated to new AWS account
        ↓
S3 global naming conflict
        ↓
S3/SQS notification validation failure
        ↓
Terraform S3/SQS dependency cycle
        ↓
SQS ReceiveMessage permission failure
        ↓
Infrastructure stabilized
        ↓
Old API Gateway ID found in frontend
        ↓
Frontend updated
        ↓
API Gateway OPTIONS returned 403
        ↓
Stale deployment discovered
        ↓
Manual deployment created
        ↓
OPTIONS returned 200
        ↓
Chat returned 401
        ↓
x-api-key added
        ↓
PowerShell request returned invalid JSON
        ↓
JSON construction fixed
        ↓
Chat RAG returned grounded response
        ↓
Crawl -> SQS -> Ingest -> DynamoDB verified
        ↓
Tenant-isolation security gap identified
        ↓
Next: tenant hardening + Terraform deployment automation
```

---

# 33. Final Assessment

The project has reached a functional end-to-end baseline.

Verified:

```text
Frontend
   ↓
API Gateway
   ↓
Authorizer
   ↓
Chat Lambda
   ↓
DynamoDB retrieval
   ↓
RAG
   ↓
Gemini
   ↓
Grounded response
```

Also verified:

```text
Crawl API
   ↓
SQS
   ↓
Ingest Lambda
   ↓
Chunking/embedding
   ↓
DynamoDB
```

The most important remaining security issue is **tenant identity enforcement**. Backend functions should use authenticated authorizer context rather than trusting `client_id` from the request body.

The most important infrastructure debt is **automatic API Gateway deployment invalidation in Terraform**.

The project should **not yet be described as production-hardened** until tenant isolation, deployment automation, observability, idempotency, and credential management are completed.

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

**Prevention:** Always test the full pipeline end-to-end after adding event sources..