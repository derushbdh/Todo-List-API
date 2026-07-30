<div align="center">
  <h1>Todo List REST API</h1>
  <p>A robust, fully tested RESTful API for task management, built with FastAPI and SQLAlchemy.</p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" />
</p>

## About The Project
This project is a backend service for a Todo List application. It demonstrates the implementation of a modern REST API including secure user authentication, database integration, data validation, and containerization. 

### Key Features
- **JWT Authentication:** Secure user registration and login with token-based auth and `bcrypt` password hashing.
- **CRUD Operations:** Full Create, Read, Update, and Delete functionality for tasks.
- **Data Validation:** Strict request/response validation using `Pydantic`.
- **Relational Database:** SQLite (easily swappable to PostgreSQL) managed via `SQLAlchemy` ORM.
- **100% Test Coverage:** Integration tests written with `Pytest`.
- **Dockerized:** Ready to be deployed anywhere using Docker.

---

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) (Recommended)
- Python 3.10+ (If running locally without Docker)

### Running with Docker (Easiest way)
1. Clone the repository:
   ```bash
   git clone https://github.com/derushbdh/Todo-List-API.git
   cd Todo-List-API
   ```
2. Build and run the container:
   ```bash
   docker build -t todo-api .
   docker run -d -p 8000:8000 todo-api
   ```
3. Open your browser and go to the interactive API documentation (Swagger UI):
   **http://localhost:8000/docs**

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/register` | Register a new user | ❌ No |
| `POST` | `/login` | Login and get JWT token | ❌ No |
| `GET`  | `/tasks` | Get all tasks for current user | ✅ Yes |
| `POST` | `/tasks` | Create a new task | ✅ Yes |
| `PUT`  | `/tasks/{id}` | Update an existing task | ✅ Yes |
| `DELETE`| `/tasks/{id}` | Delete a task | ✅ Yes |

---

## Running Tests
To run the automated tests locally:
```bash
pip install -r requirements.txt
pytest -v
```