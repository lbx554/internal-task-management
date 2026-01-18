# Internal Task Management

A simple task management system with user authentication, admin/user roles, and a web dashboard. Built with **FastAPI**, **PostgreSQL**, and a simple **HTML/JS frontend**.  

## Features

- User authentication (login)
- Admin and user roles
- Admin can create users and tasks
- Users can view their tasks
- Task statuses: `未着手`, `進行中`, `完了`
- Dashboard interface for both admin and users

---

## Project Structure

```bash
backend/
├─ app/
│ ├─ api/ # API endpoints for auth, tasks, users
│ ├─ core/ # Security, JWT, DB dependencies
│ ├─ crud/ # Database CRUD operations
│ ├─ db/ # Database models and session
│ ├─ main.py # FastAPI entrypoint
│ ├─ models/ # SQLAlchemy models
│ ├─ schemas/ # Pydantic schemas
├─ frontend/ # HTML/JS frontend (index.html, dashboard.html, main.js)
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
```

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git

> No need to install Python or PostgreSQL locally; everything runs in Docker.

---

## Setup

1. **Clone the repository:**
```bash
git clone https://github.com/lbx554/internal-task-management.git
cd internal-task-management/backend
```

2. **Create .env file in backend/:**
```bash
POSTGRES_USER=<your_postgres_user>
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_DB=<your_postgres_db>
POSTGRES_PORT=<your_postgres_port>
DATABASE_URL=postgresql://<your_postgres_user>:<your_postgres_password>@db:<your_postgres_port>/<your_postgres_db>
```

3. **Build and start containers:**
`docker-compose up --build`

This will start:
* `db`: PostgreSQL
* `api`: FastAPI backend with frontend served on `http://localhost:8000/`

4. **Access the Frontend:**
- Admin/User dashboard: `http://localhost:8000/index.html`
- Direct dashboard(if needed): `http://localhost:8000/dashboard.html`
  
---

## Admin User

You can create an admin user directly in the database or via the API:

- Example with `curl`:
```bash
curl -X POST "http://localhost:8000/api/users/" \
-H "Content-Type: application/json" \
-d '{"email": "admin@example.com", "password": "adminpass", "role": "admin"}'
```

---

## API Endpoints

- `POST /api/auth/login` -> login, returns JWT access token
- `GET /api/users/me` -> get current logged-in user
- `POST /api/users` -> create a new user (admin only)
- `GET /api/tasks/` -> list tasks
- `POST /api/tasks` -> create task (admin only)

---

## Notes

- All sensitive info (passwords, DB redentials) are stored in `.env` and ignored in `.gitignore`
- Frontend is simple HTML/JS served via FastAPI static files
- Task `created_at` and `updated_at` are still under WIP (currently showes "Undefined")

---

## Development

- Rebuild backend after changes:
`docker-compose up --build`

- Stop containers:
`docker-compose down`

 ---

 ## License
 MIT License
