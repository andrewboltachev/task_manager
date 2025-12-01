# Task Manager API

A robust, containerized REST API for task management, built with Django, DRF, and modern Python tooling (`uv`, `ruff`, `pytest`).

## 🚀 Features

*   **Task Management:** Create, read, update, and delete tasks.
*   **Assignments:** Assign tasks to specific users.
*   **Comments:** Discuss tasks via comments.
*   **Authentication:** JWT-based authentication (Access & Refresh tokens).
*   **Filtering & Search:** Filter by status/assignee, search by title/description.
*   **Documentation:** Auto-generated Swagger and Redoc UI.

## 🛠️ Tech Stack

*   **Language:** Python 3.12+
*   **Framework:** Django 5.2, Django REST Framework
*   **Database:** PostgreSQL 17
*   **Package Manager:** `uv` (Fast Python package installer)
*   **Infrastructure:** Docker & Docker Compose
*   **Linting:** Ruff
*   **Testing:** Pytest + Factory Boy
*   **Utilities:** Django-Split-Settings, Django-Extensions

## ⚙️ Installation & Setup

### Prerequisites
*   Docker & Docker Compose
*   Make (Optional, for shortcut commands)

### 1. Configure Environment
Create a `.env` file in the root directory. You can use the example configuration:

```bash
# .env
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=unsafe-dev-key-change-me

# Database (Credentials used by Docker)
POSTGRES_DB=task_manager
POSTGRES_USER=tasks_user
POSTGRES_PASSWORD=tasks_password

# Database URL (For Docker internal networking)
DATABASE_URL=postgres://tasks_user:tasks_password@db:5432/task_manager
```

### 2. Start the Application
Use the Makefile to build and start the development environment:

```bash
make dev
```
*This handles database creation, migrations, and starts the development server with hot-reloading enabled.*

The API will be available at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.

---

## 📜 Development Commands (Makefile)

This project uses a `Makefile` to simplify Docker Compose operations.

| Command | Description |
| :--- | :--- |
| **`make dev`** | Starts the application in **Development Mode** (Hot-reload, Debug=True). |
| **`make test`** | (Works when `make dev` runs) Runs the full **Pytest** suite inside the container using the test database. |
| **`make ruff`** | (Works when `make dev` runs) Runs **Ruff** to lint and auto-fix code style issues. |
| **`make bash`** | Opens a bash shell inside the running `web` container. |
| **`make prod`** | Simulates a **Production Build** (Gunicorn, Debug=False, static files collected). |
| **`make down`** | Stops all containers and removes networks. |

*If you do not have `make` installed, you can look at the `Makefile` to see the underlying `docker compose` commands.*

---

## 🧪 Testing & Linting

The project uses **Pytest** for testing and **Ruff** for linting/formatting.

### Running Tests
To ensure logic correctness (auth, permissions, CRUD):
```bash
make test
```

### Linting
To check PEP 8 compliance and code quality:
```bash
make ruff
```

---

## 📚 API Documentation

Once the server is running (`make dev`), you can access the auto-generated documentation:

*   **Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
*   **ReDoc:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
*   **OpenAPI Schema:** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

## 🔌 Django Extensions

This project includes `django-extensions`. To use advanced shell features:

1.  Enter the container:
    ```bash
    make bash
    ```
2.  Run `shell_plus` (imports all models automatically):
    ```bash
    python manage.py shell_plus
    ```
3.  Or list all URL routes:
    ```bash
    python manage.py show_urls
    ```

## 🏗 Architecture Decisions

*   **Hybrid Docker Setup:** Development uses `docker-compose.dev.yml` to mount local volumes for hot-reloading, while `docker-compose.prod.yml` uses the immutable Docker image.
*   **Root in Dev:** The development container runs as root to facilitate seamless volume mounting and package syncing (`uv sync`), while the production image runs as a secure non-root `appuser`.
*   **Settings:** Configuration is split via `django-split-settings` into `base`, `dev`, `prod`, and `test` environments for maintainability.
