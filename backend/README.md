# CloudMosaic Backend API

This is the Django backend for CloudMosaic, built with Django REST Framework and PostgreSQL.

## Prerequisites
- Python 3.12+ (Ensure your python environment has functioning pip and can build `psycopg[binary]`)
- PostgreSQL

## Local Setup (Native)

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements/development.txt
   ```
4. Copy `.env.example` to `.env` and set up your PostgreSQL credentials.
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser for the Django Admin:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the server:
   ```bash
   python manage.py runserver
   ```

## Local Setup (Docker)
If you face issues with the local Python environment (e.g. `psycopg` wheel building errors on Windows), you can use Docker:
```bash
cd backend
docker-compose up --build
```
This will automatically spin up PostgreSQL and run migrations, then start the server at `http://127.0.0.1:8000`.

To create a superuser using Docker:
```bash
docker-compose exec backend python manage.py createsuperuser
```

## URLs
- API Base: [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)
- Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- API Documentation (Swagger UI): [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)

## Known Issues
- Note: On some Windows environments using Python 3.14 (pre-release), the `psycopg` packages lack binary wheels and may fail to install natively without build tools. It is recommended to run via Docker or Python 3.12 if this error occurs.
