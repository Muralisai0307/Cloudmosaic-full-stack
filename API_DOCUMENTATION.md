# CloudMosaic API Documentation

## 1. Contact Form
Submit a general inquiry or contact form.
**Endpoint**: `POST /api/v1/contact/`
**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "service": "Cloud Migration",
  "message": "I would like to discuss a project."
}
```
**Response (201 Created)**:
```json
{
  "success": true,
  "message": "Your message has been submitted successfully.",
  "data": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "service": "Cloud Migration",
    "message": "I would like to discuss a project.",
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

## 2. Schedule Demo / Meetings
Submit a meeting request.
**Endpoint**: `POST /api/v1/meetings/`
**Request**:
```json
{
  "service": "Cloud Migration",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "1234567890",
  "company": "Tech Inc",
  "date": "2026-10-10",
  "time": "14:30",
  "notes": "Looking forward to it."
}
```
**Response (201 Created)**:
```json
{
  "success": true,
  "message": "Demo request submitted successfully.",
  "data": { ... }
}
```

## 3. Newsletter Subscription
Subscribe to the newsletter.
**Endpoint**: `POST /api/v1/newsletter/subscribe/`
**Request**:
```json
{
  "email": "test@example.com"
}
```
**Response (201 Created)**:
```json
{
  "success": true,
  "message": "Successfully subscribed to the newsletter.",
  "data": { "id": "uuid", "email": "test@example.com", "is_active": true, "created_at": "..." }
}
```

## 4. Jobs List
Retrieve active jobs.
**Endpoint**: `GET /api/v1/careers/jobs/`
**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Jobs retrieved successfully.",
  "data": [
    {
      "id": "uuid",
      "title": "Backend Engineer",
      "is_active": true,
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## 5. Job Application
Submit a job application. Use `multipart/form-data`.
**Endpoint**: `POST /api/v1/careers/jobs/apply/`
**Request (multipart/form-data)**:
- `job`: `uuid` (ID of the job)
- `name`: `string`
- `email`: `string`
- `resume`: `file (PDF, DOC, DOCX)`
- `cover_letter`: `string (optional)`

**Response (201 Created)**:
```json
{
  "success": true,
  "message": "Job application submitted successfully.",
  "data": { ... }
}
```

## 6. Services List
Retrieve active services.
**Endpoint**: `GET /api/v1/services/`
**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Services retrieved successfully.",
  "data": [
    {
      "id": "uuid",
      "title": "Cloud Migration",
      "icon": "fa-cloud",
      "description": "...",
      "tags": ["AWS", "Azure"],
      "features": ["Zero Downtime", "Cost Optimization"],
      "display_order": 1
    }
  ]
}
```

## 7. Testimonials List
Retrieve approved testimonials.
**Endpoint**: `GET /api/v1/testimonials/`
**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Testimonials retrieved successfully.",
  "data": [
    {
      "id": "uuid",
      "name": "Alice",
      "email": "alice@example.com",
      "title": "CEO",
      "service": "ERP",
      "rating": 5,
      "text": "Great work!",
      "image_url": "https://...",
      "is_approved": true,
      "created_at": "..."
    }
  ]
}
```

## 8. Testimonial / Review Submission
Submit a review.
**Endpoint**: `POST /api/v1/testimonials/`
**Request**:
```json
{
  "name": "New User",
  "email": "new@example.com",
  "service": "Design",
  "rating": 5,
  "text": "Awesome!"
}
```
**Response (201 Created)**:
```json
{
  "success": true,
  "message": "Review submitted successfully. It will appear once approved.",
  "data": { ... }
}
```
