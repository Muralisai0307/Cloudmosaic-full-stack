# Frontend to Backend Mapping

## 1. Frontend Pages & Components Discovered
- **Pages**: Home, About, Services, Products, Projects, Team, Careers, Contact, ErpComparison, Privacy, Terms, Testimonials (currently commented out but fully coded), NotFound.
- **Key Components**: ContactHub (floating chat/schedule widget), Header, Footer (newsletter).

## 2. Forms & Data Points
- **Contact Form (`/contact`)**: name, email, service, message
- **Schedule Demo Form (`ContactHub`)**: service, name, email, phone, company, date, time, notes
- **Newsletter Form (`Footer`, `Careers`)**: email
- **Job Application Form (`Careers`)**: name, email, file (resume), cover_letter, job_title
- **Review Form (`Testimonials`)**: name, email, service, rating, comment
- **Dynamic Content Lists**: Services (icon, title, tags, description, features), Testimonials (name, title, text, rating, image, date).

## 3. Backend Modules (Django Apps) Required
Based on the frontend analysis, we need the following modular apps in Django:
- `contact`
- `meetings`
- `newsletter`
- `careers`
- `services`
- `testimonials`

*Note: Blog, FAQ were not found in the frontend, and thus will be omitted to avoid unnecessary features.*

## 4. Database Models Required
1. **ContactRequest** (`contact`): name, email, service, message, created_at
2. **MeetingRequest** (`meetings`): service, name, email, phone, company, date, time, notes, created_at
3. **Subscriber** (`newsletter`): email, is_active, created_at
4. **Job** (`careers`): title, is_active, created_at
5. **JobApplication** (`careers`): job (FK), name, email, resume (FileField), cover_letter, created_at
6. **Service** (`services`): title, icon, description, tags (JSON), features (JSON), active, display_order, created_at
7. **Testimonial** (`testimonials`): name, email, title, service, rating, text, image_url, is_approved, created_at

## 5. API Endpoints Required
- `POST /api/v1/contact/` - Submit contact form
- `POST /api/v1/meetings/` - Submit schedule demo form
- `POST /api/v1/newsletter/subscribe/` - Subscribe to newsletter
- `GET /api/v1/careers/jobs/` - List active jobs
- `POST /api/v1/careers/jobs/apply/` - Submit job application (form-data for file upload)
- `GET /api/v1/services/` - List active services
- `GET /api/v1/testimonials/` - List approved testimonials
- `POST /api/v1/testimonials/` - Submit a review

## 6. Authentication Requirements
- **Public Frontend**: No user login/registration found. Public endpoints will be open (or protected by simple throttling/CORS).
- **Django Admin**: Session-based authentication for staff to manage data. DRF JWT authentication will be omitted from the frontend integration as there is no public user account functionality.

## 7. File Upload Requirements
- Job Applications require resume uploads.
- Accepted types: PDF, DOC, DOCX. Max size: 5MB (validation in both frontend and backend).
- Files will be securely stored using Django's `FileSystemStorage` or configured for S3 in production.

## 8. Frontend Changes Required
1. Update `src/services/api.js` to replace `mockApiPost` with actual `fetch`/`axios` calls pointing to the Django backend.
2. Ensure `.env` contains `REACT_APP_API_URL=http://localhost:8000/api/v1`.
3. Optionally update `Services.js` and `Testimonials.js` to fetch data from the GET endpoints instead of using static arrays.

## 9. Proposed Project Structure
```text
backend/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── contact/
│   ├── meetings/
│   ├── newsletter/
│   ├── careers/
│   ├── services/
│   └── testimonials/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env.example
├── .gitignore
└── README.md
```
