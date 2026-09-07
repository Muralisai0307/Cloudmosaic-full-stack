# CloudMosaic — Enterprise Cloud & Digital Solutions Full-Stack Platform

[![CI / Production Readiness](https://github.com/Muralisai0307/Cloudmosaic-full-stack/actions/workflows/production-readiness.yml/badge.svg)](https://github.com/Muralisai0307/Cloudmosaic-full-stack/actions)
[![Django](https://img.shields.io/badge/Django-5.2%20LTS-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17-red?logo=django)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-009639?logo=nginx&logoColor=white)](https://nginx.org/)

Production-grade, enterprise web platform for **CloudMosaic IT Services LLC** (`https://cloudmosaic.ai/`), featuring cloud migration consulting, digital transformation, custom tooling, and business HR solutions.

---

## 🏛️ System Architecture

```text
                                  Client Browser
                                        │
                                        ▼
                              Cloudflare Edge (TLS)
                                        │
                                        ▼
                                 Nginx Reverse Proxy
                               (Reverse Proxy & Static)
                                  │             │
                    ┌─────────────┘             └─────────────┐
                    ▼                                         ▼
            React 19 SPA (Build)                      Gunicorn WSGI Server
        (HashRouter / SEO / Context)                            │
                                                                ▼
                                                    Django 5.2 LTS + DRF
                                                   (Apps: Contact, Careers,
                                                    Meetings, Newsletter,
                                                    Services, Testimonials)
                                                                │
                                                                ▼
                                                        PostgreSQL 16 Database
```

---

## 📁 Repository Structure

```text
.
├── .github/workflows/          # Automated CI pipeline (lint, test, security audit)
├── backend/                    # Django 5.2 LTS + Django REST Framework API
│   ├── apps/                   # Django domain applications
│   │   ├── careers/            # Job listings & job application processing
│   │   ├── contact/            # Enterprise inquiry forms
│   │   ├── meetings/           # Scheduling wizard & meeting booking
│   │   ├── newsletter/         # Newsletter subscriptions & preferences
│   │   ├── services/           # Service catalog & pricing
│   │   └── testimonials/       # Client testimonials & reviews
│   ├── config/                 # Settings (base, development, production), URLs, WSGI/ASGI
│   ├── requirements/           # Locked dependency manifests (base, dev, prod)
│   ├── Dockerfile              # Hardened multi-stage non-root container
│   └── manage.py
├── cloudmosaic-react-main/     # React 19 Frontend Application
│   ├── public/                 # Favicons, SEO robots.txt, sitemap.xml, site manifests
│   └── src/
│       ├── components/         # Shared components, Skeleton loaders, ContactHub
│       ├── context/            # Global Toast Notification context
│       ├── pages/              # Lazy-loaded route views
│       └── services/           # Centralized API service layer
├── nginx/                      # Production Nginx reverse proxy configuration
├── scripts/                    # Automated PostgreSQL backups & restore scripts
├── docker-compose.yml          # Staging / Production multi-container orchestration
├── API_DOCUMENTATION.md        # Complete REST API specification
├── DATABASE_DESIGN.md          # PostgreSQL schemas, models, and indexing
├── FRONTEND_BACKEND_MAPPING.md # React-to-Django API integration reference
└── CloudMosaic Backend API.postman_collection.json # Ready-to-import Postman suite
```

---

## 🚀 Getting Started

### Option 1: Quickstart with Docker Compose (Recommended for Staging)

1. Copy the environment variables:
   ```bash
   cp .env.staging.example .env
   ```
2. Build and launch all services:
   ```bash
   docker compose up --build -d
   ```
3. Run migrations and create an admin user:
   ```bash
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py createsuperuser
   ```
4. Access the platform:
   - **Frontend Application**: `http://localhost:80`
   - **Backend API**: `http://localhost:80/api/v1/`
   - **Django Admin**: `http://localhost:80/admin/`

---

### Option 2: Local Development Setup

#### 1. Backend (Django + DRF)
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Configure environment
cp .env.example .env

# Run database migrations & start server
python manage.py migrate
python manage.py runserver
```
Backend API will be running at: `http://127.0.0.1:8000/api/v1/`

#### 2. Frontend (React 19)
```bash
cd cloudmosaic-react-main

# Install dependencies
npm install

# Start development server
npm start
```
Frontend will be running at: `http://localhost:3000/`

---

## 📚 Technical Documentation

- **[API Documentation](API_DOCUMENTATION.md)**: Full endpoint reference, request/response formats, status codes, and error models.
- **[Database Architecture](DATABASE_DESIGN.md)**: Schema definitions, relational constraints, foreign keys, and indexes.
- **[Frontend-to-Backend Integration](FRONTEND_BACKEND_MAPPING.md)**: API contract mapping between React services and Django endpoints.
- **[Postman Collection](CloudMosaic%20Backend%20API.postman_collection.json)**: Complete postman collection for API validation.

---

## 🛡️ Security & Hardening Highlights

- **Django Security Headers**: Strict CSP, HSTS (`preload`, `includeSubDomains`), secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`), and `X-Frame-Options: DENY`.
- **Validation & Anti-Abuse**: Server-side rate limiting (Anon 30/min, User 120/min), anti-tampering validators, and strict regex filters.
- **Docker Security**: Multi-stage lightweight builds running under an unprivileged non-root user (`appuser`).
- **Zero Secrets in Repository**: Full secret isolation using `.gitignore` and `.env` template architectures.

---

## 🧪 Automated Testing

```bash
# Run backend test suite
cd backend
python manage.py test

# Run frontend tests
cd cloudmosaic-react-main
npm test -- --watchAll=false
```

---

## 📄 License & Maintainer

Maintained for **CloudMosaic IT Services LLC**. All rights reserved.
