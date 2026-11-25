# Assignment 13 – JWT Authentication, Front-End & Playwright E2E

FastAPI application with JWT-based user registration and login, HTML front-end
pages, Playwright end-to-end tests, and a GitHub Actions CI/CD pipeline that
pushes the Docker image to Docker Hub.

- **Docker Hub:** https://hub.docker.com/r/jing212/assignment13-is601
- **GitHub Repo:** https://github.com/Jing212/assignment13-IS601

## Features

- `POST /auth/register` – validates input with Pydantic, rejects duplicate username/email, hashes the password, stores the user (201). Errors return 400/422.
- `POST /auth/login` – verifies the hashed password and returns a JWT (access + refresh token). Invalid credentials return **401**.
- `GET /register` and `GET /login` – front-end pages with client-side validation (email format, password strength, password confirmation).
- On successful login the JWT is stored in `localStorage` and the user is redirected to `/dashboard`.
- `GET /health` – health check used by Docker and CI.

Password rules: at least 8 characters, with an uppercase letter, a lowercase letter, a digit and a special character.

## Run the Application

Requirements: Docker Desktop.

```bash
docker compose up --build
```

| Page | URL |
| --- | --- |
| Register | http://localhost:8000/register |
| Login | http://localhost:8000/login |
| Dashboard | http://localhost:8000/dashboard |
| API docs (Swagger) | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |

## Run Locally Without Docker for the App

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker compose up -d db          # PostgreSQL only
uvicorn app.main:app --reload
```

## Run the Tests

Start PostgreSQL first (`docker compose up -d db`), then:

```bash
playwright install chromium      # one-time browser download

# Playwright E2E tests for the register/login pages
python -m pytest tests/e2e/test_auth_ui.py -v --no-cov

# All tests
pytest
```

> The test session drops and recreates the database tables, so users created
> manually in your local database will be removed.

### E2E test cases (`tests/e2e/test_auth_ui.py`)

| Type | Scenario | Expected result |
| --- | --- | --- |
| Positive | Register with valid data | "Registration successful" message shown |
| Positive | Log in with correct credentials | "Login successful", JWT saved in `localStorage`, redirect to `/dashboard` |
| Negative | Register with a short password | Error "at least 8 characters" shown in the UI |
| Negative | Log in with a wrong password | Server returns 401, UI shows "Invalid …" message, no token stored |

## CI/CD Pipeline

Defined in `.github/workflows/`. On every push / pull request to `main`:

1. **test** – starts a PostgreSQL service, installs dependencies and Playwright, runs unit, integration and E2E tests.
2. **security** – builds the Docker image and scans it with Trivy (fails on fixable HIGH/CRITICAL vulnerabilities).
3. **deploy** (only on `main`) – builds a multi-arch image and pushes it to Docker Hub as `latest` and the commit SHA.

The deploy job needs these secrets in the repository's `production` environment
(Settings → Environments → production):

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` (Docker Hub access token with Read & Write permission)

## Pull the Docker Image

```bash
docker pull jing212/assignment13-is601:latest
```

## Project Structure

```
app/            FastAPI app (routes, auth/JWT, models, schemas)
templates/      HTML pages (login, register, dashboard)
static/         CSS / JS
tests/          unit, integration and e2e (Playwright) tests
Dockerfile      Production image
docker-compose.yml
```

## Screenshots

Add screenshots to a `docs/` folder and link them here:

### GitHub Actions
- GitHub Actions successful run
![GitHub Actions success](docs/github-actions.png)
### Playwright E2E tests
![Playwright tests passing](docs/playwright-tests.png)

### Registration page
![Register page](docs/register-page.png)

### Login page
![Login page](docs/login-page.png)
![Dashboard with token](docs/dashboard-token.png)

## Reflection

See [REFLECTION.md](REFLECTION.md).
