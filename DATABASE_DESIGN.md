# Database Design for CloudMosaic

This document outlines the PostgreSQL database schema for the CloudMosaic backend, designed to seamlessly integrate with the existing React frontend.

## 1. Tables & Columns

### 1.1. `contact_contactrequest`
Stores submissions from the Contact Us form.
* **id** (UUID, Primary Key)
* **name** (VARCHAR(255), Not Null)
* **email** (VARCHAR(255), Not Null)
* **service** (VARCHAR(100), Not Null)
* **message** (TEXT, Not Null)
* **created_at** (TIMESTAMP, Auto Now Add)

### 1.2. `meetings_meetingrequest`
Stores submissions from the "Schedule Demo" / ContactHub form.
* **id** (UUID, Primary Key)
* **service** (VARCHAR(100), Not Null)
* **name** (VARCHAR(255), Not Null)
* **email** (VARCHAR(255), Not Null)
* **phone** (VARCHAR(50), Nullable)
* **company** (VARCHAR(255), Nullable)
* **date** (DATE, Not Null)
* **time** (TIME, Not Null)
* **notes** (TEXT, Nullable)
* **created_at** (TIMESTAMP, Auto Now Add)

### 1.3. `newsletter_subscriber`
Stores newsletter subscriptions.
* **id** (UUID, Primary Key)
* **email** (VARCHAR(255), Unique, Not Null)
* **is_active** (BOOLEAN, Default True)
* **created_at** (TIMESTAMP, Auto Now Add)
* **updated_at** (TIMESTAMP, Auto Now)

### 1.4. `careers_job`
Stores active job listings.
* **id** (UUID, Primary Key)
* **title** (VARCHAR(255), Not Null)
* **is_active** (BOOLEAN, Default True)
* **created_at** (TIMESTAMP, Auto Now Add)
* **updated_at** (TIMESTAMP, Auto Now)

### 1.5. `careers_jobapplication`
Stores submitted job applications.
* **id** (UUID, Primary Key)
* **job_id** (UUID, Foreign Key to `careers_job`, On Delete CASCADE)
* **name** (VARCHAR(255), Not Null)
* **email** (VARCHAR(255), Not Null)
* **resume** (VARCHAR(255), FileField path, Not Null)
* **cover_letter** (TEXT, Nullable)
* **created_at** (TIMESTAMP, Auto Now Add)

### 1.6. `services_service`
Stores service offerings to be displayed dynamically.
* **id** (UUID, Primary Key)
* **title** (VARCHAR(255), Not Null)
* **icon** (VARCHAR(100), Not Null)
* **description** (TEXT, Not Null)
* **tags** (JSONB, Not Null)
* **features** (JSONB, Not Null)
* **active** (BOOLEAN, Default True)
* **display_order** (INTEGER, Default 0)
* **created_at** (TIMESTAMP, Auto Now Add)
* **updated_at** (TIMESTAMP, Auto Now)

### 1.7. `testimonials_testimonial`
Stores client reviews/testimonials.
* **id** (UUID, Primary Key)
* **name** (VARCHAR(255), Not Null)
* **email** (VARCHAR(255), Not Null)
* **title** (VARCHAR(255), Nullable) - E.g., "CTO, TechCorp" (Admin only, or if review form is extended)
* **service** (VARCHAR(100), Not Null)
* **rating** (INTEGER, Not Null, Choices: 1-5)
* **text** (TEXT, Not Null)
* **image_url** (VARCHAR(500), Nullable) - Used since frontend currently expects a remote image URL. 
* **is_approved** (BOOLEAN, Default False) - Requires Admin approval to display.
* **created_at** (TIMESTAMP, Auto Now Add)
* **updated_at** (TIMESTAMP, Auto Now)

## 2. Relationships

The database is highly normalized and mostly flat, as each module is largely independent, matching the frontend's decoupled nature.

```text
+----------------+       1:N        +-------------------------+
| careers_job    | ---------------->| careers_jobapplication  |
+----------------+                  +-------------------------+
| id (PK)        |                  | id (PK)                 |
| title          |                  | job_id (FK)             |
| is_active      |                  | name                    |
| created_at     |                  | email                   |
| updated_at     |                  | resume                  |
+----------------+                  | cover_letter            |
                                    | created_at              |
                                    +-------------------------+
```

## 3. Database Constraints & Indexes
* **Newsletter Email Unique Constraint**: `newsletter_subscriber` ensures `email` is unique at the database level.
* **Indexing**: 
  * `is_active` on `careers_job`
  * `active` and `display_order` on `services_service`
  * `is_approved` on `testimonials_testimonial`
  * `email` on `newsletter_subscriber`
* **JSON Constraints**: `tags` and `features` in `services_service` utilize PostgreSQL's `JSONB` for optimized querying and storage.
