# FAILURE TEST REPORT

**Status:** NOT VERIFIED — DOCKER UNAVAILABLE

Because Docker and staging orchestration are unavailable locally, failure testing of the live microservices (killing DB, killing backend) cannot be executed.

## Application-Level Failures (Static Assessment)
- **Invalid API request**: Partially Verified (Django REST Framework strictly returns 400 Bad Request on invalid serializers, with `DEBUG=False` suppressing stack traces).
- **Missing required fields**: Partially Verified (DRF natively handles this safely).
- **Invalid resume type**: Verified via codebase (The `python-magic` integration in `careers/serializers.py` guarantees rejection of spoofed MIME types).
- **Anonymous resume download**: Verified via codebase (The `/internal-resumes/` block in Nginx requires X-Accel-Redirect from the Django admin view. Direct access returns 403/404).

## Infrastructure-Level Failures (Pending Docker Execution)
- Database unavailable simulation: NOT VERIFIED — DOCKER UNAVAILABLE
- Backend unavailable (Nginx 502 handling): NOT VERIFIED — DOCKER UNAVAILABLE
- Nginx restart behavior: NOT VERIFIED — DOCKER UNAVAILABLE
- Rate-limit testing: NOT VERIFIED — DOCKER UNAVAILABLE
