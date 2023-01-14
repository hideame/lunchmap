from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from main.models import Shop


class TestListView(TestCase):
    fixtures = ["users"]
    list_url = reverse_lazy("main:list")
    create_url = reverse_lazy("main:create")

    def pytaro_login(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username="pytaro"))

    def test_正常系_データなし(self):
        """初期状態では何も登録されていないことを確認"""
        self.assertEqual(Shop.objects.all().count(), 0)

    def test_正常系_list_pytaro(self):
        """トップページへ遷移できることをテスト"""
        self.pytaro_login()
        list_response = self.client.get(self.list_url)
        self.assertEqual(list_response.status_code, 200)

    def test_正常系_list_未ログイン(self):
        """トップページへ遷移できることをテスト"""
        self.client.logout()
        list_response = self.client.get(self.list_url)
        self.assertEqual(list_response.status_code, 200)

    def test_正常系_create_pytaro(self):
        """記事作成ページへ遷移できることをテスト"""
        self.pytaro_login()
        create_response = self.client.get(self.create_url)
        self.assertEqual(create_response.status_code, 200)

    def test_正常系_create_未ログイン(self):
        """記事作成ページへ遷移できないことをテスト"""
        self.client.logout()
        create_response = self.client.get(self.create_url)
        expected_url = "/accounts/login/?next=/main/create/"
        self.assertRedirects(
            create_response,
            expected_url,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
