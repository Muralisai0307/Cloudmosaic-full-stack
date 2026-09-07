# HTTPS / DNS DEPLOYMENT READINESS

**Status:** PARTIALLY VERIFIED / DEPLOYMENT REQUIRED

The internal application configurations for a secure HTTPS deployment are fully prepared, but the actual HTTPS termination requires external cloud deployment (DNS + Edge Proxy).

## Statically Verified Configuration
- `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` is configured, guaranteeing Django understands when it is behind a TLS-terminating load balancer.
- `SECURE_SSL_REDIRECT = True` is configured to force HTTP traffic to HTTPS.
- `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` are active.
- `HSTS` (HTTP Strict Transport Security) variables are active in `production.py`.
- `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` are dynamically loaded from environment variables.

## Deployment Required
The following architecture MUST be validated once the code is pushed to a staging/production server:
```text
DNS (e.g., cloudmosaic.ai)
    ↓
External Load Balancer (AWS ALB / Cloudflare) -> [TLS CERTIFICATE HERE]
    ↓
Nginx :80
    ↓
Gunicorn
    ↓
Django
```

Operations must verify:
- Valid TLS Certificates on the Load Balancer.
- The Load Balancer successfully strips the TLS and forwards the `X-Forwarded-Proto: https` header to Nginx.
- Nginx successfully passes this to Gunicorn.
- No Mixed Content warnings appear in the React frontend.
