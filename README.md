<div align="center">

# Nova RAG Platform

### Multi-Tenant Serverless AI Chatbot Infrastructure on AWS

*Deploy a branded, knowledge-grounded AI chatbot on any website in under 60 seconds*

[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat&logo=terraform&logoColor=white)](https://terraform.io)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-API-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=flat&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Live Demo](https://nova.babu-lahade.online) · [Fintech Tenant](https://fintech.babu-lahade.online) · [Healthcare Tenant](https://healthcare.babu-lahade.online) · [Store Tenant](https://store.babu-lahade.online)

</div>

---

## What This Is

Nova is a production-grade, multi-tenant RAG (Retrieval-Augmented Generation) SaaS platform built entirely on AWS serverless infrastructure. Any business can register, provide their website URL, and receive a single `<script>` tag that embeds a fully branded AI chatbot — trained exclusively on their own content — into any webpage.

The platform enforces strict tenant isolation at every layer: each client's knowledge base, API credentials, and conversation history are partitioned independently. One tenant cannot access another's data by design.

---

## Architecture
                     ┌─────────────────────────────────────────┐
                     │           INGESTION PIPELINE             │
                    │                                          │
POST /crawl │ nova-crawl S3 SQS │
─────────────► API GW ─► Lambda ──► Bucket ──► Queue ──► │
│ │ DLQ │
│ ▼ │
│ nova-ingest │
│ Lambda │
│ Chunk → Embed │
│ Gemini API │
│ │ │
│ ▼ │
│ DynamoDB │
│ content_chunks │
└─────────────────────────────────────────┘

                     ┌─────────────────────────────────────────┐
                     │              CHAT PIPELINE               │
                     │                                          │

widget.js │ CloudFront API GW Authorizer │
(any website) ────────►│ CDN Edge ─► /chat ─► Lambda ─► │
│ DynamoDB lookup │
│ │ │
│ ▼ │
│ nova-chat │
│ Lambda │
│ Vector Search │
│ Gemini 2.0 Flash │
│ │ │
│ ▼ │
│ Grounded Answer │
└─────────────────────────────────────────┘


---

## AWS Services

| Layer | Service | Purpose |
|---|---|---|
| Compute | AWS Lambda (×4) | nova-chat, nova-crawl, nova-ingest, nova-authorizer |
| API | Amazon API Gateway | REST endpoints with custom domain |
| Auth | Lambda Authorizer | Per-tenant API key validation via DynamoDB lookup |
| Storage | Amazon DynamoDB (×3) | Vector store, tenant configs, chat sessions |
| Queue | Amazon SQS + DLQ | Decoupled async ingestion with retry and dead-letter |
| Object Store | Amazon S3 | Raw crawled content, static frontend assets |
| CDN | Amazon CloudFront | Global edge delivery, OAC-secured S3 origin |
| DNS + TLS | Route 53 + ACM | `*.babu-lahade.online` wildcard certificate |
| Secrets | AWS Secrets Manager | Gemini API key, zero hardcoded credentials |
| IaC | Terraform | All resources defined as code, S3 remote state + DynamoDB locking |
| CI/CD | GitHub Actions + OIDC | Keyless AWS auth, automated plan and apply |
| Observability | CloudWatch + SNS | Dashboard, 4 alarms, email alerts |
| Tracing | AWS X-Ray | Distributed tracing across all Lambdas |
| AI | Gemini API | Embedding generation + grounded response |

---

## Tenant Isolation Model

API Key "fintech-key"
│
▼
Lambda Authorizer
│
├── DynamoDB lookup: chatbot_configs
│ WHERE api_key = "fintech-key"
│
├── Returns: client_id = "fintech"
│
▼
nova-chat Lambda
│
└── DynamoDB query: content_chunks
WHERE client_id = "fintech" ← partition key enforces isolation


The `client_id` is **never trusted from the request body**. It is extracted exclusively from the Lambda Authorizer context after API key validation. A tenant cannot impersonate another by modifying their request.

---

## Live Demo

| Tenant | URL | Bot | Knowledge Base |
|---|---|---|---|
| Platform | [nova.babu-lahade.online](https://nova.babu-lahade.online) | — | Platform landing |
| Fintech | [fintech.babu-lahade.online](https://fintech.babu-lahade.online) | NovaPay Assistant | Loans, KYC, credit cards |
| Healthcare | [healthcare.babu-lahade.online](https://healthcare.babu-lahade.online) | MediCare AI | Departments, appointments |
| Store | [store.babu-lahade.online](https://store.babu-lahade.online) | ShopAssist | Products, returns, shipping |

Each demo tenant has its own API key, knowledge base, brand color, and system prompt. Try asking the fintech bot a healthcare question — it will correctly say it has no information.

---

## Self-Service Onboarding
Client visits nova.babu-lahade.online/onboard.html
Enters: website URL, bot name, brand color
POST /onboard → nova-onboard Lambda
├── Generates unique API key
├── Stores config in DynamoDB chatbot_configs
└── Queues crawl job to SQS
Client receives <script> snippet instantly
nova-ingest processes the crawl in background (~60s)
Client pastes snippet → chatbot is live

Widget embed (what the client receives):

```html
<script
  src="https://[<!-- ADD YOUR CLOUDFRONT DOMAIN -->]/widget.js"
  data-api-key="nova_clientname_xxxxxxxxxxxx"
  data-bot-name="YourBot"
  data-brand-color="#2563eb"
></script>
```

---

## Repository Structure

multi-tenant-serverless-rag-platform/
│
├── lambda/
│ ├── nova_chat/ # Vector search + Gemini grounded answer
│ ├── nova_crawl/ # Website crawler → SQS
│ ├── nova_ingest/ # SQS consumer → chunk → embed → DynamoDB
│ ├── nova_authorizer/ # API key validation → client_id injection
│ ├── nova_onboard/ # Tenant registration + snippet generation
│ └── shared/ # embed.py, chunker.py, secret_manager.py
│
├── terraform/
│ ├── main.tf # Root module wiring
│ ├── backend.tf # S3 remote state + DynamoDB locking
│ ├── provider.tf
│ └── modules/
│ ├── IAM/ # Least-privilege roles per Lambda
│ ├── lambda/ # 5 Lambda functions + layers
│ ├── api_gateway/ # REST API + custom domain
│ ├── dynamodb/ # 3 tables with on-demand billing
│ ├── s3/ # Raw content + assets buckets
│ ├── sqs/ # Ingest queue + DLQ + redrive policy
│ ├── cloudwatch/ # Dashboard + 4 alarms + SNS
│ ├── eventbridge/ # Weekly scheduled re-crawl
│ ├── secrets_manager/# Gemini API key
│ └── github_oidc/ # OIDC provider + role for CI/CD
│
├── frontend/
│ ├── index.html # Platform landing page
│ ├── onboard.html # Self-service client onboarding
│ ├── fintech.html # Fintech demo site
│ ├── healthcare.html # Healthcare demo site
│ └── store.html # Store demo site
│
├── widget/
│ └── widget.js # Drop-in chat bubble (served via CloudFront)
│
├── local-api/ # Phase 1-2 local Python RAG prototype
│ ├── app.py
│ ├── rag.py
│ ├── embed.py
│ ├── chunker.py
│ └── retrieve.py
│
├── .github/
│ └── workflows/
│ └── build.yml # Build → Terraform plan → Terraform apply
│
├── FAILURES.md # Real incidents and resolutions
└── README.md


---

## CI/CD Pipeline

Push to main
│
▼
GitHub Actions
│
├── Configure AWS via OIDC (no static credentials)
├── Build Lambda packages (zip per function)
├── Upload artifacts
├── terraform init
├── terraform validate
├── terraform plan
└── terraform apply (main branch only)


Authentication uses AWS OIDC federation. The GitHub Actions runner assumes an IAM role via a short-lived token — no AWS access keys are stored in GitHub Secrets.

---

## Observability

**CloudWatch Dashboard** (`nova-rag-dashboard`):
- Chat Lambda invocations
- Chat Lambda p99 latency
- Chat Lambda error count
- SQS queue depth
- DLQ message count

**Alarms (SNS email on breach):**

| Alarm | Threshold | Meaning |
|---|---|---|
| `nova-dlq-depth` | > 0 messages | Ingest job failed all retries |
| `nova-queue-age` | > 300 seconds | Ingest Lambda stuck or throttled |
| `nova-chat-errors` | > 5 errors / 5min | Chat pipeline degraded |
| `nova-chat-duration` | p99 > 8000ms | Response latency unacceptable |

**X-Ray tracing** enabled on all 5 Lambda functions for end-to-end distributed trace visibility.

---

## Infrastructure Deployment

```bash
# Prerequisites: AWS CLI configured, Terraform >= 1.6

git clone https://github.com/BabuLahade/multi-tenant-serverless-rag-platform
cd multi-tenant-serverless-rag-platform/terraform

terraform init
terraform plan   -var="aws_region=ap-south-1" \
                 -var="project_name=nova-rag"  \
                 -var="environment=dev"

terraform apply  -var="aws_region=ap-south-1" \
                 -var="project_name=nova-rag"  \
                 -var="environment=dev"
```

Remote state is stored in S3 with DynamoDB locking — safe for team use and concurrent runs.

---

## Local Development (Phase 1-2 prototype)

```bash
git clone https://github.com/BabuLahade/multi-tenant-serverless-rag-platform
cd multi-tenant-serverless-rag-platform

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

cp .env.example .env
# Add your GEMINI_API_KEY

cd local-api
uvicorn app:app --reload

# Test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What documents are needed for KYC?", "client_id": "fintech"}'
```

---

## Environment Variables

| Variable | Used By | Description |
|---|---|---|
| `GEMINI_API_KEY` | Secrets Manager | Gemini embedding + chat model key |
| `AWS_REGION` | All Lambdas | Deployment region (ap-south-1) |
| `CONFIGS_TABLE` | authorizer, chat | DynamoDB chatbot configs table name |
| `VECTORS_TABLE` | ingest, chat | DynamoDB vector storage table name |
| `SQS_QUEUE_URL` | crawl, onboard | Ingest queue URL |
| `API_GATEWAY_URL` | onboard | Base API URL for snippet generation |

---

## FAILURES.md

Real bugs encountered during this build are documented in [FAILURES.md](FAILURES.md) — including root cause analysis and prevention steps. This includes the DynamoDB table name mismatch, IAM policy scoping errors, CORS misconfiguration, and Lambda import failures.

---

## Author

**Babu Lahade**
Final-year MCA (Cloud Computing) — Savitribai Phule Pune University
Cloud & DevOps Engineer Intern — WebcreateHub

[![GitHub](https://img.shields.io/badge/GitHub-BabuLahade-181717?style=flat&logo=github)](https://github.com/BabuLahade)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/YOUR_LINKEDIN)

---

<div align="center">
<sub>Built with AWS Lambda · API Gateway · DynamoDB · SQS · CloudFront · Terraform · GitHub Actions · Gemini API</sub>
</div>