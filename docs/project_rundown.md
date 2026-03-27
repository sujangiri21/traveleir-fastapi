# Project Rundown: FastAPI Trip API

This project is a high-performance FastAPI microservice designed to integrate seamlessly with an existing Laravel-based ecosystem. It primarily focuses on managing and retrieving "packages" (treks, trips, or travel bundles) and their associated attributes from a shared MySQL database.

## 🚀 Context and Goal
The core objective was to build a modern, asynchronous API that can provide specialized data retrieval for a trip management platform. Key highlights include:
- **Shared Database**: Directly interacts with the Laravel application's MySQL database (`trip-traveleir`).
- **High Performance**: Built with **FastAPI** and **SQLAlchemy (Async)** to ensure non-blocking I/O and low response latency.
- **Microservice Ready**: Designed to coexist with the main Laravel monolith, handling specific high-load or data-intensive tasks.

---

## 🛠️ Technology Stack
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python's modern, high-performance web framework).
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) with **AsyncIO** support.
- **Database Driver**: [aiomysql](https://github.com/aio-libs/aiomysql) (Async MySQL driver).
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/) for robust schemas.
- **Setup**: `pydantic-settings` for environment-based configuration and `.env` management.

---

## 📂 Project Structure
```text
/home/g1r/projects/fast-api-trip/
├── app/
│   ├── api/                # API versioning and endpoint controllers
│   │   ├── deps.py         # Shared dependencies (like DB session management)
│   │   └── v1/             # API v1 routes
│   │       ├── api.py      # Aggregated API router
│   │       └── endpoints/  # Specific endpoint logic (e.g., packages.py)
│   ├── core/               # Core configuration (DB connection, settings)
│   ├── crud/               # Create, Read, Update, Delete logic (data access layer)
│   ├── models/             # SQLAlchemy Database models
│   ├── schemas/            # Pydantic data schemas (input/output validation)
│   └── main.py             # Entry point of the FastAPI application
├── docs/                   # Project documentation
├── .env                    # Environment variables (Database credentials, etc.)
└── pyproject.toml          # Project dependencies (managed by uv)
```

---

## 💾 Core Models

### `Package`
The main entity representing a trip or trekking package.
- **Table**: `packages` (Laravel convention).
- **Key Fields**: `uuid`, `name`, `subtitle`, `description`, `is_active`, `is_complete`.
- **Relationship**: 1:1 relationship with `PackageAttribute`.

### `PackageAttribute`
Contains specific details about a package.
- **Table**: `package_attributes`.
- **Key Fields**: `price`, `accommodation`, `duration`, `difficulty_type_id`, `itinerary_title`, etc.
- **Relationship**: Belongs to a `Package`.

---

## 🔗 API Endpoints

### 1. Paginated Package List
**Endpoint**: `GET /api/v1/packages/`  
**Purpose**: Retrieve all packages with their associated attributes, supporting pagination.  
**Parameters**:
- `page`: Page number (default: 1).
- `size`: Items per page (default: 10, max: 100).
**Response Model**: `PackageList` (contains `items`, `total`, `page`, `size`, `pages`).

### 2. Single Package Detail
**Endpoint**: `GET /api/v1/packages/{id}`  
**Purpose**: Get detailed information for a specific package by its primary key ID.  
**Response Model**: `PackageRead` (includes nested `attribute` object).

---

## 🛠️ Setup and Running
1. **Configure Database**: Ensure your `.env` file contains correct DB credentials:
   ```env
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_DATABASE=trip-traveleir
   DB_USERNAME=admin
   DB_PASSWORD=password
   ```
2. **Install Dependencies**: Using `uv` (recommended):
   ```bash
   uv sync
   ```
3. **Run the App**:
   ```bash
   uv run fastapi dev app/main.py
   ```
4. **Interactive Docs**: Access Swagger UI at `http://127.0.0.1:8000/docs`.

---

## 🔮 Future Roadmap
- [ ] Add authentication integration (e.g., JWT if shared with Laravel or an external provider).
- [ ] Implement caching (Redis) for high-traffic package endpoints.
- [ ] Add filters and search capabilities to the packages list.
- [ ] Implement write operations (creating/updating packages) if necessary.

---
*Documentation generated on 2026-03-27*
