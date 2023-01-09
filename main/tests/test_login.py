from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy


class TestLogin(TestCase):
    fixtures = ["users"]
    list_url = reverse_lazy("main:list")

    def admin_login(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username="admin"))

    def pytaro_login(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username="pytaro"))

    def pyjiro_login(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username="pyjiro"))

    def test_正常系_admin_login(self):
        self.admin_login()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_正常系_pytaro_login(self):
        self.pytaro_login()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_正常系_pyjiro_login(self):
        self.pyjiro_login()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_正常系_未ログイン(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_正常系_admin_管理画面(self):
        self.admin_login()
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/admin/main/shop/")
        self.assertEqual(response.status_code, 200)

    def test_異常系_pytaro_管理画面(self):
        self.pytaro_login()
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/admin/main/shop/")
        self.assertEqual(response.status_code, 403)

    def test_異常系_未ログイン_管理画面(self):
        self.client.logout()
        response = self.client.get("/admin/")
        expected_url = "/admin/login/?next=/admin/"
        self.assertRedirects(
            response, expected_url, status_code=302, target_status_code=200, msg_prefix="", fetch_redirect_response=True
        )
