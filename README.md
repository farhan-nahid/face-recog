# AK AWS Face Recognition Service

[![Python Version](https://img.shields.io/badge/python-3.14.2-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.123.0-05998b.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-23.0.0-00D4AA.svg?logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.38.0-000000.svg?logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Boto3](https://img.shields.io/badge/Boto3-1.42.0-FF9900.svg?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/sdk-for-python/)
[![AWS Rekognition](https://img.shields.io/badge/AWS-Rekognition-FF9900.svg?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/rekognition/)
[![DigitalOcean Spaces](https://img.shields.io/badge/DigitalOcean%20Spaces-Enabled-0080FF.svg?logo=digitalocean&logoColor=white)](https://www.digitalocean.com/products/spaces/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-316192.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.45-D70206.svg?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.18.0-F8D210.svg?logo=alembic&logoColor=black)](https://alembic.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Loguru](https://img.shields.io/badge/Loguru-Logging-00D9FF.svg)](https://github.com/Delgan/loguru)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-6BA539.svg?logo=openapi-initiative&logoColor=white)](https://www.openapis.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-green.svg)](https://github.com/)
[![Production Ready](https://img.shields.io/badge/Production-Ready-brightgreen.svg)](https://github.com/)
[![API Docs](https://img.shields.io/badge/API-Documented-blue.svg?logo=swagger-ui&logoColor=white)](http://localhost:8000/docs)

A high-performance, production-ready microservice built with **FastAPI**, **AWS Rekognition**, and **PostgreSQL**. This service provides a robust API for facial recognition, face indexing, and management of face collections and **SQLAlchemy** with **Alembic** for reliable database management.

---

## 📋 Table of Contents

| Section                                               | Description                        |
| :---------------------------------------------------- | :--------------------------------- |
| [🚀 Key Features](#-key-features)                     | Core capabilities and features     |
| [🛠 Tech Stack](#-tech-stack)                         | Technologies and frameworks used   |
| [🏗 System Architecture](#-system-architecture)       | High-level architecture diagram    |
| [⚙️ Prerequisites](#️-prerequisites)                   | Requirements before installation   |
| [📦 Installation & Setup](#-installation--setup)      | Step-by-step setup guide           |
| [📖 API Documentation](#-api-documentation)           | Interactive API docs and endpoints |
| [📂 Project Structure](#-project-structure)           | Directory and file organization    |
| [🏛 Architecture Deep Dive](#-architecture-deep-dive) | Core modules and services layer    |
| [🚀 Production Features](#-production-features)       | Production-ready configurations    |
| [🤝 Contributing](#-contributing)                     | Contribution guidelines            |
| [📄 License](#-license)                               | Proprietary license information    |
| [📞 Support & Maintainer](#-support--maintainer)      | Contact information                |

---

## 🚀 Key Features

- **Advanced Facial Recognition:** High-accuracy face detection and matching using **AWS Rekognition**.
- **Face Liveness Detection:** Integrated AWS Rekognition Face Liveness for anti-spoofing verification with temporary credential generation for secure frontend integration.
- **Robust Database:** **PostgreSQL** backend with **SQLAlchemy** ORM for structured data management.
- **Database Migrations:** Automated schema management using **Alembic**.
- **High Performance:** Built on **FastAPI** for rapid request processing and asynchronous capabilities.
- **Containerization:** Fully dockerized with multi-stage Alpine Linux builds for development and production.
- **Comprehensive Facade:**
  - **Collection & Face Management:** Create, delete, and manage AWS Rekognition collections and faces.
  - **Face Indexing:** Upload and index images directly to cloud storage.
  - **Search & Identification:** Identify individuals with adjustable confidence thresholds.
  - **Face Record Database:** Complete CRUD operations with soft delete, restore, and pagination support.
- **Production Ready:**
  - **Structured Logging:** JSON-formatted logs via `Loguru` with request tracking and client IP detection (supports Cloudflare, nginx, AWS ALB).
  - **Health Monitoring:** Liveness and readiness probes for Kubernetes orchestration.
  - **CORS Configured:** Ready for frontend integration with configurable origins.
  - **Reverse Proxy Support:** Configured for deployment behind reverse proxies with subpath routing.
  - **Gunicorn + Uvicorn:** Production-grade ASGI server with multiple workers for high availability.

---

## 🛠 Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) 0.123.0
- **Runtime:** [Python 3.14.2](https://python.org) (Optimized with Alpine Linux 3.22 for Docker)
- **AWS SDK:** [Boto3](https://aws.amazon.com/sdk-for-python/) 1.42.0 (Rekognition, S3, STS)
- **Database:** [PostgreSQL](https://www.postgresql.org/) 18
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) 2.0.45
- **Migrations:** [Alembic](https://alembic.sqlalchemy.org/) 1.18.0
- **Validation:** [Pydantic v2](https://docs.pydantic.dev/) 2.12.5
- **Logging:** [Loguru](https://github.com/Delgan/loguru) 0.7.3
- **Server:** [Gunicorn](https://gunicorn.org/) 23.0.0 + [Uvicorn](https://www.uvicorn.org/) 0.38.0
- **Deployment:** Docker & Docker Compose with Multi-Stage Builds

---

## 🏗 System Architecture

```mermaid
graph TB
    subgraph Client
        Browser["Web/Mobile Client"]
    end

    subgraph "FastAPI Microservice"
        API["FastAPI App (Uvicorn)"]
        Middleware["Logging & CORS Middleware"]
        Router["API Routers"]

        subgraph "Services Layer"
            FaceService["Face Service"]
            RecService["Recognition Service"]
            DBService["Database Service"]
        end
    end

    subgraph "Data & External Infrastructure"
        PG[(PostgreSQL Database)]
        Rekognition["AWS Rekognition"]
    end

    Browser -->|HTTPS/JSON| API
    API --> Middleware
    Middleware --> Router

    Router --> FaceService
    Router --> RecService
    Router --> DBService

    FaceService -->|Index/Search| Rekognition
    RecService -->|Search| Rekognition

    FaceService -->|Metadata| DBService
    FaceService -->|Images

    DBService -->|SQLAlchemy| PG
```

---

## ⚙️ Prerequisites

Before running the services, ensure you have the following:

- **Python 3.14.2+** (for local development)
- **PostgreSQL Database** (Local or Remote)
  - Connection details:
    - `DB_HOST`
    - `DB_PORT`
    - `DB_USER`
    - `DB_PASSWORD`
    - `DB_NAME`
- **AWS Account** (Rekognition Access)
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
- **Application Settings**
  - `PORT`
  - `LOG_LEVEL`
  - `ENVIRONMENT`
  - `CORS_ALLOWED_ORIGINS`

- **Docker & Docker Compose** (Optional, for containerized deployment)

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://git.evidentbd.com/attendance-keeper/backend/ak-aws-face-rec-service.git
cd ak-aws-face-rec-service
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your AWS credentials:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# AWS credentials and settings
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# PostgreSQL database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_NAME=face_recognition_db

# Application settings
PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

```

### 3. Database Setup

Initialize the database schema using Alembic:

```bash
# Apply migrations
alembic upgrade head
```

### 4. Local Development (Standard)

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
cd src
uvicorn main:app --reload --port 8000
```

### 5. Running with Docker

**Development Mode:**

```bash
# Build and start with hot-reload
docker compose -f docker-compose.dev.yml up --build

# Check logs
docker compose -f docker-compose.dev.yml logs -f
```

**Production Mode:**

```bash
# Build and start the production container
docker compose up --build -d

# Check logs
docker compose logs -f
```

**Note:** The service is configured with `root_path="/face-rec"` for reverse proxy deployments. Adjust this in [main.py](src/main.py) if deploying at a different path.

---

## 📖 API Documentation

Once the service is running, you can access the interactive API documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Core Endpoints Preview

**Health Check**
| Method | Endpoint | Description |
| :----- | :-------- | :------------------- |
| `GET` | `/api/v1/health` | General health check |
| `GET` | `/api/v1/health/liveness` | Kubernetes liveness probe |
| `GET` | `/api/v1/health/readiness` | Kubernetes readiness probe (DB check) |

**Collection Management**
| Method | Endpoint | Description |
| :------- | :-------------------------------- | :--------------------------------- |
| `POST` | `/api/v1/collection` | Create a new collection |
| `GET` | `/api/v1/collection` | List all collections |
| `GET` | `/api/v1/collection/{collection_name}` | Get collection details |
| `DELETE` | `/api/v1/collection/{collection_name}` | Delete a collection |

**Face Management**
| Method | Endpoint | Description |
| :------- | :---------------------------------------- | :------------------------------------- |
| `POST` | `/api/v1/face` | Add a face to collection (file upload) |
| `GET` | `/api/v1/face` | List faces with pagination |
| `GET` | `/api/v1/face/{collection_name}/{face_id}` | Get specific face details |
| `PUT` | `/api/v1/face/{collection_name}/{external_image_id}` | Update a face (file upload) |
| `DELETE` | `/api/v1/face/{collection_name}/{external_image_id}` | Delete a face |

**Liveness Detection (Anti-Spoofing)**
| Method | Endpoint | Description |
| :----- | :-------------------------------------------------- | :------------------------------------------------------------ |
| `POST` | `/api/v1/liveness/temporary-credentials` | Generate temporary AWS STS credentials for secure frontend liveness SDK integration |
| `POST` | `/api/v1/liveness` | Create a new Face Liveness session (returns SessionId) |
| `GET` | `/api/v1/liveness/{session_id}/{collection_name}` | Get liveness session results with face recognition match (optional threshold) |

**Face Recognition**
| Method | Endpoint | Description |
| :----- | :-------------------- | :------------------------------------ |
| `POST` | `/api/v1/recognition` | Recognize face from uploaded image |

**Face Record Management (Database)**
| Method | Endpoint | Description |
| :------- | :-------------------------------------------------------------- | :------------------------------------- |
| `GET` | `/api/v1/face-record/id/{record_id}` | Get record by Database ID |
| `GET` | `/api/v1/face-record/external/{collection}/{image_id}` | Get record by External Image ID |
| `GET` | `/api/v1/face-record/aws-face/{collection}/{aws_face_id}` | Get record by AWS Face ID |
| `GET` | `/api/v1/face-record/employee/{company_id}/{employee_id}` | Get records by Employee |
| `GET` | `/api/v1/face-record/company/{company_id}` | List company records (Paginated) |
| `PATCH` | `/api/v1/face-record/{record_id}` | Update face record metadata |
| `DELETE` | `/api/v1/face-record/{record_id}` | Soft delete a record |
| `DELETE` | `/api/v1/face-record/{record_id}/permanent` | **Hard delete** a record |
| `POST` | `/api/v1/face-record/{record_id}/restore` | Restore a soft-deleted record |
| `GET` | `/api/v1/face-record/deleted` | List all deleted records |
| `GET` | `/api/v1/face-record/deleted/company/{company_id}` | List deleted records by company |

---

## 📂 Project Structure

```text
ak-aws-face-rec-service/
├── .env.example
├── .gitlab-ci.yml
├── Dockerfile
├── Dockerfile.dev
├── LICENSE
├── README.md
├── alembic.ini
├── docker-compose.dev.yml
├── docker-compose.yml
├── requirements.txt
├── sonar-project.properties
└── src/
    ├── alembic/            # Database configurations
    │   ├── versions/       # Migration scripts
    │   ├── env.py
    │   └── script.py.mako
    ├── apis/               # API Router and View implementations
    │   ├── collection/     # Collection management routes
    │   ├── face/           # Face CRUD and indexing routes
    │   ├── face_record/    # Local DB FaceRecord management (CRUD with soft delete)
    │   ├── health/         # Health/Liveness/Readiness probes for K8s
    │   ├── liveness/       # AWS Face Liveness detection routes
    │   └── recognition/    # Face matching and recognition routes
    ├── core/               # Configuration and common utilities
    │   ├── database.py     # Database connection & session
    │   ├── logging_*.py    # Logging config & middleware
    │   ├── models.py       # SQLAlchemy Models (FaceRecord)
    │   ├── response.py     # Response patterns
    │   ├── schema.py       # Common Schemas
    │   ├── settings.py     # Environment settings
    │   └── validators.py   # Input validators
    ├── services/           # Business Logic Layer
    │   ├── aws/            # AWS Rekognition/S3 wrappers
    │   ├── database/       # Database CRUD services
    └── main.py             # FastAPI entry point
```

---

## 🗄️ Database Models

The service uses **PostgreSQL** with **SQLAlchemy** ORM. Below is the schema for the core `FaceRecord` model.

### `FaceRecord` Model

Represents a face indexed in AWS Rekognition and stored in the local database.

| Field               | Type       | Required | Description                         |
| :------------------ | :--------- | :------- | :---------------------------------- |
| `id`                | `UUID`     | Yes      | Unique Primary Key (auto-generated) |
| `company_id`        | `String`   | Yes      | Tenant/Company identifier           |
| `employee_id`       | `String`   | Yes      | Employee identifier                 |
| `external_image_id` | `String`   | No       | External reference ID               |
| `aws_collection_id` | `String`   | Yes      | AWS Rekognition Collection ID       |
| `aws_image_id`      | `String`   | Yes      | AWS Rekognition Image ID            |
| `aws_face_id`       | `String`   | Yes      | AWS Rekognition Face ID             |
| `image_url`         | `String`   | No       | URL to the stored image             |
| `confidence`        | `Float`    | No       | Face detection confidence score     |
| `meta_data`         | `JSON`     | No       | Additional arbitrary metadata       |
| `created_at`        | `DateTime` | Yes      | Creation timestamp                  |
| `updated_at`        | `DateTime` | Yes      | Last update timestamp               |
| `deleted_at`        | `DateTime` | No       | Soft deletion timestamp             |

---

## 🔄 Database Migrations

Database schema changes are managed with **Alembic**.

### Common Commands

```bash
# Create a new migration revision
alembic revision --autogenerate -m "description_of_changes"

# Apply all pending migrations
alembic upgrade head

# Revert the last migration
alembic downgrade -1

# Show current revision
alembic current
```

---

## 🏛 Architecture Deep Dive

The application follows a clean, layered architecture to ensure separation of concerns and scalability.

### 1. API Layer (`src/apis/`)

- **Role**: Handles incoming HTTP requests, input validation, and response formatting.
- **Components**:
  - **Routers**: FastAPI routers organized by domain (collection, face, recognition).
  - **Schemas**: Pydantic models for request/response validation.
  - **Middleware**: Logging and CORS handling.

### 2. Service Layer (`src/services/`)

- **Role**: Encapsulates business logic and orchestration.
- **Components**:
  - **AWS Service**: Wraps Boto3 calls to Rekognition and S3 (`src/services/aws/`).
  - **Database Service**: Manages CRUD operations using SQLAlchemy.

### 3. Core Layer (`src/core/`)

- **Role**: Provides shared utilities and configuration.
- **Components**:
  - **Settings**: Centralized environment variable management using Pydantic Settings (`src/core/settings.py`).
  - **Models**: SQLAlchemy database models with UUID primary keys and soft delete support (`src/core/models.py`).
  - **Validators**: Reusable validation logic (e.g., file types, image formats).
  - **Logging**: Structured JSON logging with request tracking, client IP extraction (Cloudflare/proxy support), and middleware (`src/core/logging_config.py`, `src/core/logging_middleware.py`).
  - **Database**: Connection pooling and health check utilities (`src/core/database.py`).
  - **Response**: Standardized response formatting for success and error cases (`src/core/response.py`).

---

## 🚀 Production Features

### Request Logging & Monitoring

The service includes comprehensive request logging middleware that captures:

- Unique request IDs (8-character UUID)
- HTTP method, route, and status code
- Request duration in milliseconds
- Client IP address (with support for Cloudflare `CF-Connecting-IP`, `X-Forwarded-For`, `X-Real-IP` headers)
- User agent information
- Structured JSON logs for easy parsing and monitoring

### Reverse Proxy & Subpath Deployment

The application is configured with `root_path="/face-rec"` for deployment behind reverse proxies. This ensures:

- OpenAPI docs work correctly at `https://domain.com/face-rec/docs`
- API routes are properly prefixed
- Easy integration with Kubernetes ingress, nginx, or Cloudflare

### Health Checks for Kubernetes

- **Liveness Probe:** `/api/v1/health/liveness` - Always returns 200 OK
- **Readiness Probe:** `/api/v1/health/readiness` - Verifies database connectivity

### Docker Multi-Stage Build

- **Builder Stage:** Compiles dependencies with all build tools
- **Runtime Stage:** Minimal Alpine image (~200MB) with only runtime dependencies
- **Security:** Non-root user (appuser:1000), no unnecessary packages
- **Performance:** Python bytecode compilation, **pycache** cleanup

### Production Server Configuration

Runs with Gunicorn + Uvicorn workers:

```bash
gunicorn main:app \
  --bind 0.0.0.0:8000 \
  -w 1 \
  -k uvicorn.workers.UvicornWorker \
  --access-logfile - \
  --error-logfile -
```

Adjust `-w` parameter based on CPU cores: `(2 x num_cores) + 1`

---

## 🤝 Contributing

1. Clone the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Merge Request

---

## 📄 License

This is a **proprietary software project** owned by **Evident BD**. All rights reserved.

### ⚖️ License Type: Proprietary

This software is **NOT open source**. It is the confidential and proprietary property of Evident BD.

### 📋 Usage Rights

✅ **Authorized Users CAN:**

- Use the software for internal business purposes within Evident BD
- Access the software as authorized by Evident BD management
- Deploy the software on approved infrastructure

❌ **Restrictions - You CANNOT:**

- Copy, modify, or create derivative works without authorization
- Reverse engineer, decompile, or disassemble the software
- Distribute, sublicense, or transfer the software to third parties
- Remove or alter copyright notices
- Use the software outside of authorized scope
- Share source code with external parties

### 🔒 Confidentiality

This software contains valuable trade secrets and proprietary information. All users must:

- Maintain strict confidentiality of the source code
- Not disclose any part of the software to unauthorized parties
- Follow company information security policies

### 📜 Full License Terms

For complete license terms and conditions, please see the [LICENSE](LICENSE) file.

### 📧 License Inquiries

For licensing questions or authorization requests, contact:

- **Email:** support@evidentbd.com
- **Company:** Evident BD

---

## 📞 Support & Maintainer

Maintained by **Evident BD**.
For support, please contact [support@evidentbd.com](mailto:support@evidentbd.com) or open an issue in the repository.

---

<p align="center">Made with ❤️ by Evident BD</p>
