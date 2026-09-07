from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from .models import Job, JobApplication

class CareerTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.list_url = reverse('job-list')
        self.apply_url = reverse('job-apply')
        
        self.active_job = Job.objects.create(title="Backend Engineer", is_active=True)
        self.inactive_job = Job.objects.create(title="Frontend Engineer", is_active=False)

    def test_active_jobs_returned(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Backend Engineer")

    def test_valid_application(self):
        pdf_content = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
        resume = SimpleUploadedFile("resume.pdf", pdf_content, content_type="application/pdf")
        payload = {
            "job": self.active_job.id,
            "name": "Applicant",
            "email": "applicant@example.com",
            "resume": resume
        }
        response = self.client.post(self.apply_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 1)

    def test_invalid_resume_type(self):
        resume = SimpleUploadedFile("resume.txt", b"file_content", content_type="text/plain")
        payload = {
            "job": self.active_job.id,
            "name": "Applicant",
            "email": "applicant@example.com",
            "resume": resume
        }
        response = self.client.post(self.apply_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('resume', response.data['errors'])

    def test_missing_job(self):
        resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        payload = {
            "name": "Applicant",
            "email": "applicant@example.com",
            "resume": resume
        }
        response = self.client.post(self.apply_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('job', response.data['errors'])

    def test_anonymous_user_cannot_download_resume(self):
        resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        app = JobApplication.objects.create(job=self.active_job, name="App", email="a@b.com", resume=resume)
        download_url = reverse('resume-download', kwargs={'pk': app.id})
        response = self.client.get(download_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_admin_can_download_resume(self):
        from django.contrib.auth.models import User
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        self.client.force_authenticate(user=admin_user)
        
        resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        app = JobApplication.objects.create(job=self.active_job, name="App", email="a@b.com", resume=resume)
        download_url = reverse('resume-download', kwargs={'pk': app.id})
        
        response = self.client.get(download_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('X-Accel-Redirect', response.headers)
        self.assertTrue(response.headers['X-Accel-Redirect'].startswith('/internal-resumes/'))

    def test_exe_renamed_to_pdf_rejected(self):
        # DOS/Windows PE executable binary signature renamed as .pdf
        exe_content = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00\xb8\x00\x00\x00"
        resume = SimpleUploadedFile("malicious.pdf", exe_content, content_type="application/pdf")
        payload = {
            "job": self.active_job.id,
            "name": "Attacker",
            "email": "attacker@example.com",
            "resume": resume
        }
        response = self.client.post(self.apply_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('resume', response.data['errors'])

    def test_html_renamed_to_pdf_rejected(self):
        html_content = b"<!DOCTYPE html><html><body><script>alert(1)</script></body></html>"
        resume = SimpleUploadedFile("exploit.pdf", html_content, content_type="application/pdf")
        payload = {
            "job": self.active_job.id,
            "name": "Attacker",
            "email": "attacker@example.com",
            "resume": resume
        }
        response = self.client.post(self.apply_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('resume', response.data['errors'])

    def test_oversized_resume_rejected(self):
        # 5.5MB file (limit is 5MB)
        large_content = b"%PDF-1.4\n" + b"0" * (5500 * 1024)
        resume = SimpleUploadedFile("large.pdf", large_content, content_type="application/pdf")
        payload = {
            "job": self.active_job.id,
            "name": "Applicant",
            "email": "applicant@example.com",
            "resume": resume
        }
        response = self.client.post(self.apply_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('resume', response.data['errors'])
