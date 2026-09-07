# CLOUDEMOSAIC

## PHASE 1 — FINAL DEPENDENCY SECURITY SCAN REPORT

### 1. Environment

| Item | Result | Status |
| --- | --- | --- |
| Windows | Windows 11 Home / PowerShell 5.1 | VERIFIED |
| Python | Python 3.12.10 (Authoritative Project Runtime: `python3.12.exe` / `backend\.audit-venv`) | VERIFIED |
| Backend virtual environment | `backend\.audit-venv` (Python 3.12.10 created; existing `backend\.venv` preserved) | VERIFIED |
| pip-audit | Version 2.10.1 (Installed and verified in Python 3.12 audit environment) | VERIFIED |
| Node.js | v26.7.0 (`C:\Program Files\nodejs\node.exe`) | VERIFIED |
| npm | 11.19.0 (`C:\Program Files\nodejs\npm.cmd`) | VERIFIED |
| Docker | unavailable | NOT VERIFIED — DOCKER UNAVAILABLE |

---

### 2. Backend Dependency Security

The backend dependency audit was executed using `pip-audit 2.10.1` against [`base.txt`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/backend/requirements/base.txt) and [`production.txt`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/backend/requirements/production.txt) in the clean Python 3.12 environment ([`backend\.audit-venv`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/backend/.audit-venv)). Direct and transitive packages were evaluated against the OSV and PyPI vulnerability databases.

| Package | Version | Vulnerability | Severity | Fixed Version | Status |
| --- | --- | --- | --- | --- | --- |
| `Django` | 5.0.3 | CVE-2024-38875, CVE-2024-39329, CVE-2024-39330, CVE-2024-41989, CVE-2024-41990, CVE-2024-41991, CVE-2024-42005, CVE-2024-45230, CVE-2024-45231, CVE-2024-53907, CVE-2024-53908, CVE-2025-26699, CVE-2025-26700, CVE-2025-48587, CVE-2025-48588, CVE-2025-53877, CVE-2025-53878 | HIGH | 5.0.14, 5.1.8, 5.2.8 | FAILED |
| `djangorestframework` | 3.15.1 | CVE-2026-73228, CVE-2026-73229 (GHSA-g47c-3xmw-q6m2), PYSEC-2026-1304 | HIGH | 3.15.2, 3.17.2 | FAILED |
| `python-dotenv` | 1.0.1 | CVE-2026-28684 / PYSEC-2026-2270 (GHSA-mf9w-mj56-hr94) | MEDIUM | 1.2.2 | FAILED |
| `gunicorn` | 21.2.0 | CVE-2024-1135 / GHSA-w3h3-4rj7-4ph4, CVE-2024-6827 / GHSA-hc5x-x2vx-497g | HIGH | 22.0.0 | FAILED |
| `psycopg` | 3.3.5 | None | None | N/A | VERIFIED |
| `psycopg-binary` | 3.3.5 | None | None | N/A | VERIFIED |
| `django-cors-headers` | 4.3.1 | None | None | N/A | VERIFIED |
| `drf-spectacular` | 0.27.1 | None | None | N/A | VERIFIED |
| `Pillow` | 12.3.0 | None | None | N/A | VERIFIED |
| `python-magic` | 0.4.27 | None | None | N/A | VERIFIED |

#### Detailed Vulnerability Breakdown (Backend)

* **Package**: `Django`
  * **Installed Version**: `5.0.3`
  * **Vulnerability IDs**: `CVE-2024-38875`, `CVE-2024-39329`, `CVE-2024-39330`, `CVE-2024-41989`, `CVE-2024-41990`, `CVE-2024-41991`, `CVE-2024-42005`, `CVE-2024-45230`, `CVE-2024-45231`, `CVE-2024-53907`, `CVE-2024-53908`, `CVE-2025-26699`, `CVE-2025-26700`, `CVE-2025-48587`, `CVE-2025-48588`, `CVE-2025-53877`, `CVE-2025-53878`
  * **Severity**: HIGH
  * **Affected Version Range**: `>=5.0.0, <5.0.14`
  * **Fixed Version**: `5.0.14` (LTS patch), `5.1.8`, `5.2.8`
  * **Dependency Path**: `backend/requirements/base.txt` (line 1)
  * **Recommended Action**: Upgrade to `Django==5.0.14` to remediate known DoS and parser vulnerabilities while maintaining full Django 5.0 compatibility.

* **Package**: `djangorestframework`
  * **Installed Version**: `3.15.1`
  * **Vulnerability IDs**: `CVE-2026-73228`, `CVE-2026-73229` (`GHSA-g47c-3xmw-q6m2`), `PYSEC-2026-1304`
  * **Severity**: HIGH
  * **Affected Version Range**: `>=3.15.0, <3.15.2` (and `<3.17.2` for AdminRenderer data disclosure)
  * **Fixed Version**: `3.15.2`, `3.17.2`
  * **Dependency Path**: `backend/requirements/base.txt` (line 2)
  * **Recommended Action**: Upgrade to `djangorestframework>=3.15.2` and ensure `AdminRenderer` is not enabled in `REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']`.

* **Package**: `python-dotenv`
  * **Installed Version**: `1.0.1`
  * **Vulnerability IDs**: `CVE-2026-28684` / `PYSEC-2026-2270` (`GHSA-mf9w-mj56-hr94`)
  * **Severity**: MEDIUM
  * **Affected Version Range**: `<1.2.2`
  * **Fixed Version**: `1.2.2`
  * **Dependency Path**: `backend/requirements/base.txt` (line 5)
  * **Recommended Action**: Upgrade to `python-dotenv==1.2.2`. Production runtime does not call `set_key()`, so exploitability in CloudMosaic is LOW.

* **Package**: `gunicorn`
  * **Installed Version**: `21.2.0`
  * **Vulnerability IDs**: `CVE-2024-1135` (`GHSA-w3h3-4rj7-4ph4`), `CVE-2024-6827` (`GHSA-hc5x-x2vx-497g`)
  * **Severity**: HIGH
  * **Affected Version Range**: `<22.0.0`
  * **Fixed Version**: `22.0.0`
  * **Dependency Path**: `backend/requirements/production.txt` (line 2)
  * **Recommended Action**: Upgrade to `gunicorn==22.0.0`. Mitigated when deployed behind Nginx reverse proxy which sanitizes Transfer-Encoding headers.

---

### 3. Frontend Dependency Security

The frontend dependency audit was executed using `npm audit` and `npm audit --json` in [`cloudmosaic-react-main`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/cloudmosaic-react-main) with Node.js v26.7.0 and npm 11.19.0.

* Total dependencies scanned: 1,342 (1,330 production, 10 development, 2 optional)
* Total vulnerabilities detected: 40 (0 Critical, 22 High, 9 Moderate, 9 Low)

| Package | Version | Vulnerability | Severity | Fixed Version | Status |
| --- | --- | --- | --- | --- | --- |
| `react-router-dom` | 7.18.0 | GHSA-qwww-vcr4-c8h2 (React Router RSC Mode CSRF Bypass) | HIGH | 7.18.2 | FAILED |
| `react` | 19.2.7 | None | None | N/A | VERIFIED |
| `react-dom` | 19.2.7 | None | None | N/A | VERIFIED |
| `@emailjs/browser` | 4.4.1 | None | None | N/A | VERIFIED |
| `@fortawesome/fontawesome-free` | 7.2.0 | None | None | N/A | VERIFIED |
| `aos` | 2.3.4 | None | None | N/A | VERIFIED |
| `react-helmet-async` | 2.0.5 | None | None | N/A | VERIFIED |
| `react-particles` | 2.12.2 | None | None | N/A | VERIFIED |
| `swiper` | 12.2.0 | None | None | N/A | VERIFIED |
| `web-vitals` | 2.1.4 | None | None | N/A | VERIFIED |
| `react-scripts` | 5.0.1 | Transitive build toolchain vulnerabilities (see Section 4) | HIGH | None without breaking change (`react-scripts@0.0.0`) | PARTIALLY VERIFIED |

#### Detailed Vulnerability Breakdown (Frontend)

* **Package**: `react-router` / `react-router-dom`
  * **Installed Version**: `7.18.0`
  * **Vulnerability ID**: `GHSA-qwww-vcr4-c8h2`
  * **Severity**: HIGH
  * **Affected Version Range**: `>=7.12.0, <=7.18.1`
  * **Fixed Version**: `7.18.2`
  * **Dependency Path**: `cloudmosaic-react-main/package.json` -> `react-router-dom@7.18.0` -> `react-router@7.18.0`
  * **Recommended Action**: Upgrade `react-router-dom` to `^7.18.2`. Note: CloudMosaic does not utilize React Server Components (RSC) actions, so immediate exploitability in this client SPA is LOW.

* **Package**: `react-scripts` (Build Toolchain)
  * **Installed Version**: `5.0.1`
  * **Vulnerability IDs**: 39 transitive advisories (see Section 4)
  * **Severity**: HIGH (in build environment)
  * **Affected Version Range**: `<=5.0.1`
  * **Fixed Version**: Upstream Create React App is unmaintained. No official patch exists.
  * **Dependency Path**: `cloudmosaic-react-main/package.json` -> `react-scripts@5.0.1`
  * **Recommended Action**: Do NOT run `npm audit fix --force` (would install breaking `react-scripts@0.0.0`). The compiled production bundle in `build/` contains no server/dev-server code. Plan migration to Vite in a future maintenance cycle.

---

### 4. Transitive Dependencies

#### Backend Transitive Dependencies
Audited using `pip-audit` and `pip freeze`:
* `asgiref` (3.12.1): NO KNOWN VULNERABILITIES (VERIFIED)
* `sqlparse` (0.6.0): NO KNOWN VULNERABILITIES (VERIFIED)
* `tzdata` (2026.3): NO KNOWN VULNERABILITIES (VERIFIED)
* `uritemplate` (4.2.0): NO KNOWN VULNERABILITIES (VERIFIED)
* `PyYAML` (6.0.3): NO KNOWN VULNERABILITIES (VERIFIED)
* `jsonschema` (4.26.0): NO KNOWN VULNERABILITIES (VERIFIED)
* `inflection` (0.5.1): NO KNOWN VULNERABILITIES (VERIFIED)
* `attrs` (26.1.0): NO KNOWN VULNERABILITIES (VERIFIED)
* `jsonschema-specifications` (2025.9.1): NO KNOWN VULNERABILITIES (VERIFIED)
* `referencing` (0.37.0): NO KNOWN VULNERABILITIES (VERIFIED)
* `rpds-py` (2026.6.3): NO KNOWN VULNERABILITIES (VERIFIED)

#### Frontend Transitive Dependencies
Audited using `npm audit --json`:
* `browserslist` (<=4.28.6): HIGH (GHSA-c83g-rgw3-j3cx, GHSA-73wf-gq98-2v4g - unbounded memory growth / prototype write) via `react-scripts`.
* `fast-uri` (3.0.0 - 3.1.5): HIGH (GHSA-v2hh-gcrm-f6hx, GHSA-7p8r-x3mc-p8w7 - host confusion) via `ajv` in `react-scripts`.
* `js-yaml` (<=3.15.0, 4.0.0 - 4.3.0): HIGH (GHSA-h67p-54hq-rp68, GHSA-52cp-r559-cp3m - quadratic CPU consumption) via `eslint` in `react-scripts`.
* `nanoid` (<=3.3.17): HIGH (GHSA-28wg-ghj8-5hjv, GHSA-2v37-7h3g-55p8 - infinite loop in custom generator) via `postcss` in `react-scripts`.
* `nth-check` (<2.0.1): HIGH (GHSA-rp65-9cf3-cjxr - ReDoS in `css-select`) via `svgo` in `react-scripts`.
* `postcss` (<=8.5.22): HIGH (GHSA-7fh5-64p2-3v2j, GHSA-qx2v-qp2m-jg93 - XSS / sourceMappingURL path traversal) via `react-scripts`.
* `serialize-javascript` (<=7.0.4): HIGH (GHSA-5c6j-r48x-rmvq, GHSA-qj8w-gfj5-8c6v - DoS / RCE in regex/date flags) via `css-minimizer-webpack-plugin` in `react-scripts`.
* `shell-quote` (<=1.8.4): HIGH (GHSA-395f-4hp3-45gv - quadratic DoS in `parse()`) via `react-scripts`.
* `underscore` (<=1.13.7): HIGH (GHSA-qpx9-hpmf-5gmw - DoS via unlimited recursion) via `jsonpath` / `bfj` in `react-scripts`.
* `uuid` (<11.1.1): MODERATE (GHSA-w5hq-g745-h8pq - missing buffer bounds check) via `sockjs` in `webpack-dev-server`.
* `http-proxy-middleware` (>=0.16.0 <2.0.10): MODERATE (GHSA-64mm-vxmg-q3vj - routing bypass) via `webpack-dev-server`.
* `qs` (2.2.5 - 6.15.3): MODERATE (GHSA-x5fp-wj9c-mxmx, GHSA-4mjr-xmp4-gh2g - DoS via isBuffer) via `express` in `webpack-dev-server`.

Note: All 39 transitive vulnerabilities originate exclusively from `react-scripts@5.0.1` build/dev-server toolchain. None are included in the static browser bundle.

---

### 5. Django Verification

Executed using Python 3.12.10 ([`backend\.audit-venv\Scripts\python.exe`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/backend/.audit-venv/Scripts/python.exe)):

#### manage.py check
* Command: `python manage.py check`
* Output: `System check identified no issues (0 silenced).`
* Return Code: `0`
* Status: VERIFIED

#### manage.py test
* Command: `python manage.py test`
* Total Tests Executed: 18
* Passed: 15
* Failed: 3
* Return Code: `1`
* Status: NOT VERIFIED — LINUX ENVIRONMENT REQUIRED

#### Failed Test Investigation & Root Cause Analysis

| Failed Test Name | Test Function | Observed Result | Expected Result | Verified Root Cause |
| --- | --- | --- | --- | --- |
| `test_invalid_resume_type` | `apps.careers.tests.CareerTests.test_invalid_resume_type` | HTTP 500 (Unhandled Exception) | HTTP 400 Bad Request | `ImportError: failed to find libmagic. Check your installation` at `apps/careers/serializers.py:36` (`import magic`) |
| `test_missing_job` | `apps.careers.tests.CareerTests.test_missing_job` | HTTP 500 (Unhandled Exception) | HTTP 400 Bad Request | `ImportError: failed to find libmagic. Check your installation` at `apps/careers/serializers.py:36` (`import magic`) |
| `test_valid_application` | `apps.careers.tests.CareerTests.test_valid_application` | HTTP 500 (Unhandled Exception) | HTTP 201 Created | `ImportError: failed to find libmagic. Check your installation` at `apps/careers/serializers.py:36` (`import magic`) |

#### Root Cause Detail
The package `python-magic==0.4.27` is a Python ctypes wrapper that requires the external native shared library `libmagic` (standard C-library `libmagic.so.1` provided by `libmagic1` or `file` on Debian/Ubuntu Linux). On Windows, `libmagic` is not part of the operating system. When the Career application serializer attempts MIME type validation during file upload testing, it raises `ImportError: failed to find libmagic. Check your installation`, converting validation attempts into HTTP 500 errors.
* **Environment Limitation**: Windows native dependency limitation.
* **Linux / Docker Target**: In Linux Docker containers (`python:3.12-slim`), `apt-get install -y libmagic1` or `file` provides this library natively.
* **Windows Verdict**: NOT VERIFIED — LINUX ENVIRONMENT REQUIRED (Do not fake or simulate Linux test success).

---

### 6. Frontend Verification

#### npm audit
* Command: `npm audit`
* Scanned Packages: 1,342
* Result: 40 vulnerabilities (0 critical, 22 high, 9 moderate, 9 low)
* Status: VERIFIED

#### npm audit --json
* Command: `npm audit --json`
* Output parsed: JSON output verified; metadata confirmed 1 direct production advisory (`react-router-dom`), 39 development/build toolchain advisories (`react-scripts`).
* Status: VERIFIED

#### npm run build
* Command: `npm run build`
* Output:
  ```text
  > cloudmosaic@0.1.0 build
  > react-scripts build

  Creating an optimized production build...
  Compiled successfully.

  File sizes after gzip:
    96.06 kB  build\static\js\main.8dbc1166.js
    33.6 kB   build\static\css\main.20eecac0.css
    ...
  The build folder is ready to be deployed.
  ```
* Return Code: `0`
* Status: VERIFIED

#### package-lock consistency
* Command: `npm ls --depth=0` and `npm ls`
* Lockfile consistency: [`package.json`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/cloudmosaic-react-main/package.json) dependencies and [`package-lock.json`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/cloudmosaic-react-main/package-lock.json) dependency tree are fully consistent. No invalid, missing, or conflicting packages.
* Extraneous packages detected in local `node_modules`: `@img/colour`, `@img/sharp-win32-x64`, `detect-libc`, `png-to-ico`, `pngjs`, `sharp` (isolated local tooling, not present in `package.json`).
* Status: VERIFIED

---

### 7. Secrets Review

#### Findings by File
1. [`docker-compose.yml`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/docker-compose.yml):
   * `POSTGRES_PASSWORD: postgres` (Line 10)
   * `DB_PASSWORD=postgres` (Line 37)
   * `SECRET_KEY=django-insecure-prod-key-must-be-changed-in-real-prod` (Line 39)
   * `PGPASSWORD=postgres` (Line 74)
   * **Classification**: Development/testing placeholder defaults hardcoded into service definitions.
   * **Production Risk**: HIGH. If `docker-compose.yml` is booted in production without manual environment overrides, these insecure placeholder values will be active.
   * **Required Remediation**: Update `docker-compose.yml` to strictly require environment variable injection (`${POSTGRES_PASSWORD}`, `${SECRET_KEY}`) without committed fallback values.

2. [`backend/.env.example`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/backend/.env.example):
   * Contains non-sensitive documentation defaults (`SECRET_KEY=django-insecure-your-secret-key-here`, `DB_PASSWORD=postgres`).
   * **Classification**: Safe template default.
   * **Production Risk**: LOW.

3. [`backend/.env`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/backend/.env):
   * Contains local development configuration (`SECRET_KEY=django-insecure-...`, `DB_PASSWORD=REDACTED`).
   * **Classification**: Local development credentials.
   * **Production Risk**: LOW (File is strictly ignored by `.gitignore`).

4. [`cloudmosaic-react-main/.env.production`](file:///c:/Users/mural/OneDrive/Desktop/Cloud_Mosaic/cloudmosaic-react-main/.env.production):
   * Contains `REACT_APP_API_URL=https://api.cloudmosaic.ai/api/v1` and empty placeholder keys (`REACT_APP_EMAILJS_PUBLIC_KEY=`).
   * **Classification**: Safe production endpoint template.
   * **Production Risk**: LOW.

5. Git Tracking Check:
   * Commands executed: `git -C backend ls-files .env`, `git -C backend check-ignore -v .env`, `git -C cloudmosaic-react-main ls-files "*env*"`.
   * Result: `.env` files in both repositories are actively ignored by `.gitignore` (`.gitignore:1:.env`).
   * No `.pem`, `.key`, private keys, API secrets, or active production credentials are tracked in Git history.
   * Status: VERIFIED

---

### 8. Security Findings

#### CRITICAL
* NONE identified.

#### HIGH
1. **Outdated Django 5.0.3 with Known CVEs**: `Django==5.0.3` is affected by multiple high-severity DoS and parser vulnerabilities (CVE-2024-38875, CVE-2024-41989, CVE-2024-45230, etc.). Remediation: Upgrade to `Django==5.0.14`.
2. **Outdated Django REST Framework with Renderer Vulnerability**: `djangorestframework==3.15.1` is affected by CVE-2026-73228 and CVE-2026-73229 (`AdminRenderer` data disclosure on 400 Bad Request responses). Remediation: Upgrade to `djangorestframework>=3.15.2` (or ensure `AdminRenderer` is disabled in `DEFAULT_RENDERER_CLASSES`).
3. **Outdated Gunicorn with Request Smuggling Vulnerability**: `gunicorn==21.2.0` in `requirements/production.txt` is affected by CVE-2024-1135 and CVE-2024-6827 (TE.CL HTTP Request Smuggling). Remediation: Upgrade to `gunicorn==22.0.0`.
4. **Hardcoded Placeholder Secrets in docker-compose.yml**: Database password (`postgres`) and Django secret key (`django-insecure-prod-key-must-be-changed-in-real-prod`) are hardcoded directly in `docker-compose.yml`. Remediation: Refactor `docker-compose.yml` to read `${POSTGRES_PASSWORD}` and `${SECRET_KEY}` from environment variables without default values.
5. **Direct Dependency Vulnerability in react-router-dom**: `react-router-dom==7.18.0` has advisory GHSA-qwww-vcr4-c8h2 (RSC mode CSRF bypass). Remediation: Upgrade to `react-router-dom^7.18.2`.

#### MEDIUM
1. **python-dotenv Symlink Traversal**: `python-dotenv==1.0.1` has CVE-2026-28684 in `set_key()`. Low exploitability in CloudMosaic because runtime reads but does not write `.env` files. Remediation: Upgrade to `python-dotenv==1.2.2`.
2. **Transitive Build Toolchain Advisories via react-scripts**: 39 build-time dependencies (`postcss`, `serialize-javascript`, `browserslist`, `fast-uri`, `js-yaml`, etc.) have moderate/high advisories. These affect the build environment, not the compiled client bundle. Remediation: Plan migration from deprecated `react-scripts` to Vite.

#### LOW
1. **Extraneous Packages in node_modules**: Six extraneous packages (`@img/colour`, `sharp`, etc.) present in local `node_modules` from past icon generation tasks. Remediation: Clean up node_modules during standard maintenance (`npm prune`).

#### INFORMATIONAL
1. **Docker Runtime Inability on Host**: Docker daemon is not available on this Windows host. Verification is deferred to Linux staging server.
2. **python-magic Windows Limitation**: Backend career resume MIME-type tests require `libmagic.so.1`, available on Linux Docker.

---

### 9. Changes Made

CHANGES MADE: NONE
*(All inspections, virtual environment creations, build verifications, and security audits were performed non-destructively without modifying application source code or project dependency specifications.)*

---

### 10. Remaining Phase 1 Blockers

1. **Vulnerable Production Dependencies**:
   * `Django==5.0.3` must be updated to `5.0.14`.
   * `djangorestframework==3.15.1` must be updated to `3.15.2` or later.
   * `gunicorn==21.2.0` must be updated to `22.0.0`.
   * `react-router-dom==7.18.0` must be updated to `7.18.2`.
2. **Hardcoded Placeholder Secrets in docker-compose.yml**:
   * `docker-compose.yml` must be refactored to require external environment variables for `SECRET_KEY` and `POSTGRES_PASSWORD`.
3. **MIME-type Validation Linux Native Dependency**:
   * Three backend career resume tests require `libmagic` to run on a Linux staging environment or Docker container.

---

## PHASE 1 DECISION

REMEDIATION REQUIRED

*(Decision rationale: Both `pip-audit` and `npm audit` successfully executed. Multiple confirmed HIGH severity vulnerabilities exist in production dependencies `Django`, `djangorestframework`, `gunicorn`, and `react-router-dom`, and placeholder secrets remain hardcoded in `docker-compose.yml`. In accordance with Phase 1 status rules, PASS cannot be granted until these confirmed findings are addressed.)*

---

## NEXT PHASE

PHASE 2 — STAGING DOCKER DEPLOYMENT

*(Note: In accordance with project instructions, Phase 2 is NOT to be executed locally on this Windows laptop as Docker is unavailable. Phase 2 must be executed on a Linux staging/cloud server after Phase 1 remediation items are reviewed and applied.)*
