# TrustMesh-AI

> Production-oriented backend foundation for a secure, multi-tenant AI knowledge intelligence platform.

TrustMesh-AI is a backend foundation designed for an AI-powered knowledge intelligence platform. The current implementation establishes the core infrastructure required before adding advanced retrieval, RAG, agent, and knowledge-processing workloads.

The project focuses on **secure identity, JWT authentication, organization isolation, membership management, role-based authorization, asynchronous PostgreSQL persistence, database migration discipline, and automated engineering quality gates**.

Rather than coupling business logic directly to HTTP handlers or database queries, TrustMesh-AI uses a layered architecture built around:

- FastAPI
- Pydantic
- SQLAlchemy 2
- PostgreSQL
- Alembic
- JWT authentication
- Organization membership
- Role-based authorization
- Repository/service separation
- Automated testing
- Ruff
- mypy

The architecture is intentionally designed so that future AI capabilities can be added without turning the backend into a tightly coupled monolith.

---

## Project Status

**Submission-ready backend foundation.**

Current verified state:

| Quality Gate | Result |
|---|---|
| Automated tests | **81 passed** |
| Ruff linting | **Passed** |
| Ruff formatting | **59 files already formatted** |
| mypy | **0 errors** |
| Alembic current revision | **b88c9d32a540** |
| Alembic migration head | **b88c9d32a540** |
| Git working tree | **Clean before README update** |

The current implementation provides the secure backend foundation required for future organization-scoped AI workloads.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Core Capabilities](#core-capabilities)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Authentication](#authentication)
- [Authorization](#authorization)
- [Organization Model](#organization-model)
- [API Surface](#api-surface)
- [Technology Stack](#technology-stack)
- [Database](#database)
- [Configuration](#configuration)
- [Local Development](#local-development)
- [Docker Infrastructure](#docker-infrastructure)
- [Database Migrations](#database-migrations)
- [Testing](#testing)
- [Engineering Quality Gates](#engineering-quality-gates)
- [Security Considerations](#security-considerations)
- [Engineering Principles](#engineering-principles)
- [Future Scope](#future-scope)
- [Repository](#repository)

---

## Project Overview

TrustMesh-AI is designed around a simple architectural principle:

> **Build the secure backend foundation first, then attach AI intelligence to well-defined boundaries.**

The current system establishes:

1. User identity
2. Authentication
3. JWT security
4. Organization isolation
5. Membership management
6. Role-based permissions
7. Database persistence
8. API validation
9. Migration management
10. Automated regression testing

This foundation can later support systems such as:

- Trusted document ingestion
- Knowledge bases
- Vector search
- Retrieval-Augmented Generation
- AI agents
- Background document processing
- Organization-scoped knowledge retrieval
- AI workflow orchestration
- Audit and permission systems

Those capabilities are future extensions. The current implementation focuses on the backend security and tenancy foundation required to support them correctly.

---

## Core Capabilities

### Identity and Authentication

TrustMesh-AI currently supports:

- User registration
- User login
- Password-based authentication
- JWT access tokens
- Bearer-token authentication
- Token signature validation
- Token expiration validation
- Token subject validation
- Referenced-user validation
- Invalid token rejection
- Expired token rejection
- Tampered token rejection
- Wrong-secret token rejection
- Protected API endpoints

### Organization Management

Organizations provide the foundation for multi-tenant application behavior.

Current capabilities include:

- Organization creation
- Automatic owner membership
- Organization lookup
- Organization membership creation
- Organization membership lookup
- Organization membership listing
- Duplicate membership protection
- Organization-scoped access control

### Role-Based Authorization

TrustMesh-AI currently supports four organization roles:

```text
OWNER
ADMIN
MEMBER
VIEWER
```

Authorization is implemented through reusable FastAPI dependencies.

This allows routes to express permission requirements without embedding authorization logic directly inside every endpoint.

For example, a route dependency can require specific roles (illustrative snippet — not a standalone script):

```text
# app/api/organizations.py
from app.authorization.roles import OrganizationRole
from app.dependencies.organization import require_organization_role

@router.delete("/organizations/{organization_id}")
async def delete_organization(
    membership: OrganizationMember = Depends(
        require_organization_role(
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
        )
    ),
):
    ...
```

This provides a centralized authorization boundary that can evolve as the platform grows.

---

## Architecture

TrustMesh-AI follows a layered backend architecture.

```
                         ┌─────────────────────┐
                         │       Client        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI API      │
                         │       Layer         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │ Authentication / Authorization│
                    │          Dependencies         │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │   Service Layer     │
                         │   Business Logic    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Repository Layer    │
                         │ Database Access     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ SQLAlchemy Models   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    PostgreSQL       │
                         └─────────────────────┘
```

The architecture separates:

- HTTP transport
- Authentication
- Authorization
- Business logic
- Persistence
- Database models
- Configuration
- Infrastructure

This prevents individual route handlers from becoming responsible for the entire application stack.

### Request Flow

A protected request follows this general path:

```
HTTP Request
     │
     ▼
FastAPI Router
     │
     ▼
Authentication Dependency
     │
     ├── Invalid / Missing Token ──► 401
     │
     ▼
Current User
     │
     ▼
Organization Membership Dependency
     │
     ├── Not a Member ──► 403
     │
     ▼
Role Authorization
     │
     ├── Insufficient Role ──► 403
     │
     ▼
Service Layer
     │
     ▼
Repository Layer
     │
     ▼
PostgreSQL
     │
     ▼
Validated Response
```

This flow establishes explicit security boundaries before business operations execute.

---

## Project Structure

```
TrustMesh-AI/
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── organization_members.py
│   │   ├── organizations.py
│   │   └── users.py
│   │
│   ├── authorization/
│   │   └── roles.py
│   │
│   ├── core/
│   │   └── configuration.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── organization.py
│   │
│   ├── models/
│   │   ├── organization.py
│   │   ├── organization_member.py
│   │   └── user.py
│   │
│   ├── repositories/
│   │   ├── organization.py
│   │   ├── organization_member.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── organization.py
│   │   ├── organization_member.py
│   │   └── user.py
│   │
│   ├── security/
│   │   └── token.py
│   │
│   ├── services/
│   │   ├── organization.py
│   │   ├── organization_member.py
│   │   └── user.py
│   │
│   └── main.py
│
├── docker/
├── docs/
├── scripts/
├── tests/
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## Authentication

Authentication uses JWT access tokens.

The high-level flow is:

```
User Registration
       │
       ▼
    User DB
       │
       ▼
     Login
       │
       ▼
Password Verification
       │
       ▼
JWT Access Token
       │
       ▼
Authorization Header
       │
       ▼
Token Validation
       │
       ▼
Current User
```

A protected request uses:

```
Authorization: Bearer <access-token>
```

The security layer validates the token before allowing protected application logic to execute.

### Token Validation

The security implementation validates:

- Token structure
- Token signature
- Token expiration
- Token subject
- User existence

Invalid tokens are rejected rather than being allowed to reach business logic.

The test suite specifically verifies:

```
Valid Token
    │
    └──► Accepted


Expired Token
    │
    └──► Rejected


Invalid Token
    │
    └──► Rejected


Tampered Token
    │
    └──► Rejected


Wrong-Secret Token
    │
    └──► Rejected
```

---

## Authorization

Authentication answers:

> "Who is this user?"

Authorization answers:

> "What is this user allowed to do?"

TrustMesh-AI keeps those concerns separate.

The organization authorization system is based on membership.

```
                    Organization
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
           Owner       Admin       Member
             │           │           │
             └───────────┼───────────┘
                         │
                       User
```

A user must belong to an organization before organization-scoped operations can proceed.

---

## Organization Model

The central relationship is:

```
User
 │
 │
 ▼
OrganizationMember
 │
 │
 ▼
Organization
```

An `OrganizationMember` represents the relationship between a user and an organization.

A membership contains:

| Field | Purpose |
|---|---|
| id | Unique membership identifier |
| organization_id | Organization reference |
| user_id | User reference |
| role | Organization role |
| created_at | Membership creation timestamp |

When an organization is created, the creating user automatically receives the `OWNER` role.

This establishes a predictable ownership model from the beginning.

### Organization Roles

The current authorization model defines:

| Role | Purpose |
|---|---|
| OWNER | Highest organization-level authority |
| ADMIN | Administrative organization access |
| MEMBER | Standard organization member |
| VIEWER | Read-oriented organization access |

Reusable dependencies determine whether the current membership satisfies the required role.

This prevents permission checks from being scattered throughout the API.

---

## API Surface

The current API is versioned under:

```
/api/v1
```

### Authentication

**Login**

```
POST /api/v1/auth/login
```

Authenticates a user and returns an access token.

### Users

**Create User**

```
POST /api/v1/users
```

Creates a new user account.

### Organizations

**Create Organization**

```
POST /api/v1/organizations
```

Creates an organization and establishes the authenticated user as its owner.

**Get Organization**

```
GET /api/v1/organizations/{organization_id}
```

Returns an organization accessible to the authenticated member.

### Organization Members

**Create Membership**

```
POST /api/v1/organizations/{organization_id}/members
```

Creates an organization membership.

**List Memberships**

```
GET /api/v1/organizations/{organization_id}/members
```

Lists memberships belonging to an organization.

**Get Membership**

```
GET /api/v1/organizations/{organization_id}/members/{user_id}
```

Returns a specific user's membership within an organization.

### Health

```
GET /health
```

Provides a lightweight application health endpoint.

### API Documentation

When the application is running, FastAPI provides interactive API documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```
http://127.0.0.1:8000/openapi.json
```

---

## Technology Stack

**Runtime**
- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings

**Persistence**
- PostgreSQL
- SQLAlchemy 2
- asyncpg
- Alembic

**Security**
- JWT-based authentication
- Bearer-token authorization
- Organization membership authorization
- Role-based access control

**Infrastructure**
- Docker
- Docker Compose
- Redis
- Qdrant
- Celery

**Engineering Tooling**
- pytest
- pytest-asyncio
- Ruff
- mypy
- Git
- GitHub

---

## Database

PostgreSQL is the primary persistent data store.

The application uses SQLAlchemy's asynchronous API.

The database access architecture is:

```
FastAPI
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
AsyncSession
   │
   ▼
PostgreSQL
```

This keeps database queries isolated inside repository classes.

Business logic remains in services rather than being embedded directly into SQL queries or API routes.

---

## Database Migrations

Alembic manages database schema changes.

Migrations are version controlled alongside the application.

Current verified migration state:

```
Current:
b88c9d32a540 (head)

Head:
b88c9d32a540 (head)
```

The database revision and migration head are synchronized.

To upgrade a local database:

```bash
alembic upgrade head
```

To inspect the current revision:

```bash
alembic current
```

To inspect migration heads:

```bash
alembic heads
```

---

## Configuration

Environment configuration is represented by `.env.example`.

Current configuration:

```env
APP_NAME=TrustMesh AI
APP_VERSION=0.1.0
DEBUG=true

DATABASE_URL=postgresql+asyncpg://trustmesh:trustmesh@localhost:5432/trustmesh

REDIS_URL=redis://localhost:6379/0

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=trustmesh_documents
```

For local development, create the environment file:

```powershell
Copy-Item .env.example .env
```

Then update the values according to the local infrastructure.

The `.env` file should not be committed to Git.

---

## Local Development

### Requirements

Recommended environment:

- Python 3.11
- PostgreSQL
- Git
- Docker
- Docker Compose
- PowerShell on Windows or an equivalent shell

### Clone the Repository

```bash
git clone https://github.com/arifxlab/TrustMesh-AI.git
cd TrustMesh-AI
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create `.env` from the example:

```powershell
Copy-Item .env.example .env
```

Review the database and infrastructure settings before starting the application.

### Run Migrations

```bash
alembic upgrade head
```

### Start the API

```bash
uvicorn app.main:app --reload
```

The API should then be available at:

```
http://127.0.0.1:8000
```

Health endpoint:

```
http://127.0.0.1:8000/health
```

Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Docker Infrastructure

The repository includes Docker Compose infrastructure for supporting services.

The configured infrastructure includes:

- PostgreSQL
- Redis
- Qdrant

The environment configuration maps to:

- PostgreSQL — `localhost:5432`
- Redis — `localhost:6379`
- Qdrant — `localhost:6333`

Start the infrastructure with:

```bash
docker compose up -d
```

Check running services:

```bash
docker compose ps
```

Stop the infrastructure:

```bash
docker compose down
```

The application can then connect to the infrastructure using the configured environment variables.

---

## Testing

TrustMesh-AI uses pytest for automated verification.

The test suite covers both lower-level application behavior and HTTP API behavior.

Current verified result:

```
81 passed
```

Run the complete test suite:

```bash
pytest -q
```

### Test Coverage Areas

The current suite covers:

**Authentication**
- User registration
- Login
- Authentication requirements
- Invalid authentication
- Token validation

**Security**
- Valid JWT tokens
- Expired JWT tokens
- Invalid JWT tokens
- Tampered JWT tokens
- Wrong-secret JWT tokens

**Organizations**
- Organization creation
- Organization ownership
- Organization retrieval
- Unknown organization handling
- Authentication requirements

**Memberships**
- Membership creation
- Membership retrieval
- Membership listing
- Default membership roles
- Duplicate membership protection
- Role validation
- Missing membership handling

**Authorization**
- Organization membership enforcement
- Owner authorization
- Admin authorization
- Member authorization
- Viewer restrictions
- Multi-role authorization
- Unauthorized organization access

---

## Security Considerations

Security behavior is treated as a first-class engineering concern.

The test suite explicitly verifies that security failures do not silently become successful requests.

For example:

```
Tampered JWT
     │
     ▼
Signature Validation
     │
     ▼
Invalid Signature
     │
     ▼
Authentication Rejected
```

Organization access follows:

```
Authenticated User
        │
        ▼
Organization Membership
        │
   ┌────┴────┐
   │         │
Member     Not Member
   │         │
   ▼         ▼
Continue     403
```

Role authorization then applies an additional boundary:

```
Organization Member
        │
        ▼
Required Role
        │
   ┌────┴─────┐
   │          │
Allowed    Insufficient
   │          │
   ▼          ▼
Continue      403
```

This creates defense-in-depth between authentication, tenant membership, and authorization.

---

## Engineering Quality Gates

The project uses automated quality gates before changes are considered complete.

### Ruff

Linting:

```bash
ruff check .
```

Expected result:

```
All checks passed!
```

Formatting:

```bash
ruff format --check .
```

Expected result:

```
59 files already formatted
```

### mypy

Run strict static type checking:

```bash
mypy app
```

Expected result:

```
Success: no issues found in 36 source files
```

The project enables strict mypy checking through `pyproject.toml`.

### pytest

Run the complete test suite:

```bash
pytest -q
```

Expected result:

```
81 passed
```

### Alembic

Verify the database revision:

```bash
alembic current
```

Verify migration heads:

```bash
alembic heads
```

Expected:

```
b88c9d32a540 (head)
```

for both commands.

### Git Validation

Check whitespace errors:

```bash
git diff --check
```

Check repository state:

```bash
git status
```

### Complete Verification Command Set

Before submitting or pushing a major change, run:

```bash
ruff check .
ruff format --check .
mypy app
pytest -q
alembic current
alembic heads
git diff --check
git status
```

A healthy project should report:

```
Ruff: PASS
Formatting: PASS
mypy: PASS
pytest: PASS
Alembic: synchronized
Git: clean
```

---

## Engineering Principles

TrustMesh-AI is built around production-oriented backend engineering principles.

### Separation of Concerns

API handlers should coordinate HTTP behavior rather than contain the entire business domain.

Business rules belong in services.

Database access belongs in repositories.

### Repository / Service Separation

The repository layer handles persistence.

The service layer handles business operations.

This allows database implementation details to change without rewriting API behavior.

### Explicit Authorization Boundaries

Authorization is implemented through reusable dependencies.

This avoids repeating permission checks across multiple endpoints.

### Strong Input Validation

Pydantic schemas validate incoming API data before business logic processes it.

Invalid payloads are rejected at the API boundary.

### Secure Token Handling

Authentication does not rely only on token structure.

The security layer validates:

- Signature
- Expiration
- Subject
- User existence

### Async Database Access

SQLAlchemy asynchronous sessions are used for database operations.

This establishes a foundation suitable for I/O-heavy backend workloads.

### Migration Discipline

Database schema changes are managed through Alembic.

The migration history is version controlled and verified against the active database revision.

### Automated Regression Testing

Every major backend capability has automated verification.

This reduces the risk of security and authorization regressions as the platform expands.

### Static Type Checking

Strict mypy checking is enabled.

The current application passes:

```
Success: no issues found in 36 source files
```

---

## Future Scope

TrustMesh-AI is intentionally structured as a foundation rather than a finished AI product.

Future development can build on the existing security and organization model.

Potential capabilities include:

### Document Ingestion

```
Upload
   │
   ▼
Validation
   │
   ▼
Extraction
   │
   ▼
Chunking
   │
   ▼
Embedding
   │
   ▼
Vector Store
```

### Retrieval-Augmented Generation

Future RAG workflows can use organization-scoped retrieval:

```
User
 │
 ▼
Organization
 │
 ▼
Authorized Knowledge Base
 │
 ▼
Retriever
 │
 ▼
Relevant Chunks
 │
 ▼
LLM
 │
 ▼
Grounded Response
```

### AI Agents

Future agent workflows can use the existing authorization foundation to determine which organization resources an agent is permitted to access.

Potential components include:

- Agent orchestration
- Tool execution
- Retrieval tools
- Workflow state
- Background jobs
- Audit logging

### Background Processing

The repository already includes infrastructure relevant to asynchronous processing.

Future workloads can include:

- Document processing
- Embedding generation
- Indexing
- Retrieval preparation
- AI task execution

Celery and Redis can provide the background task foundation.

### Vector Search

Qdrant is included in the infrastructure configuration.

Future document retrieval can use Qdrant for vector similarity search while organization-level authorization remains enforced by the application layer.

### Why the Architecture Matters

TrustMesh-AI is not designed as a collection of isolated CRUD endpoints.

The architecture establishes boundaries that become increasingly important as backend systems grow.

A future AI request can follow a path such as:

```
Client
  │
  ▼
Authentication
  │
  ▼
Organization Membership
  │
  ▼
Role Authorization
  │
  ▼
AI Service
  │
  ▼
Retrieval Service
  │
  ▼
Vector Database
  │
  ▼
LLM
  │
  ▼
Validated Response
```

The current implementation establishes the security boundary at the beginning of that pipeline.

That makes the system easier to extend without having to retrofit authentication and authorization after AI functionality has already been built.

### Current Limitations

The current submission focuses on the backend foundation.

The following are intentionally not represented as completed features:

- Full document ingestion pipeline
- Production RAG pipeline
- Production AI agent orchestration
- Advanced vector retrieval workflows
- AI evaluation framework
- Distributed deployment
- Observability platform
- Production secret management
- Production cloud deployment
- Full audit logging

These are future engineering stages rather than completed claims.

### Development Workflow

A typical development cycle is:

```
Requirement
    │
    ▼
Architecture
    │
    ▼
Implementation
    │
    ▼
Unit / API Tests
    │
    ▼
Ruff
    │
    ▼
mypy
    │
    ▼
Database Migration Verification
    │
    ▼
Git Diff Validation
    │
    ▼
Commit
    │
    ▼
Push
```

This workflow keeps functional correctness, security, code quality, and database state aligned.

---

## Repository

GitHub:

```
https://github.com/arifxlab/TrustMesh-AI
```

## License

This project is currently maintained as a portfolio and engineering project.

License terms can be added when the repository is prepared for public redistribution or open-source contribution.

---

## Final Verification

At the current development checkpoint, TrustMesh-AI has verified:

```
81 automated tests passed

Ruff:
All checks passed

Formatting:
59 files already formatted

mypy:
Success: no issues found in 36 source files

Alembic:
b88c9d32a540 (head)

Migration Head:
b88c9d32a540 (head)
```

TrustMesh-AI is ready for final repository submission after the README documentation update and final Git verification.