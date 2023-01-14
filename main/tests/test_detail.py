from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from main.models import Category, Shop


class TestDetailView(TestCase):
    fixtures = ["users", "category"]
    detail_url = reverse_lazy("main:detail", kwargs={"pk": 1})
    update_url = reverse_lazy("main:update", kwargs={"pk": 1})

    def setUp(self):
        self.pytaro_login()
        user = User.objects.get(username="pytaro")
        category = Category.objects.get(name="中華料理")
        shop = Shop(name="炎神", address="茨城県水戸市桜川2-1-6アイランドビル1F", author_id=user.id, category_id=category.id)
        shop.save()

    def pytaro_login(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username="pytaro"))

    def pyjiro_login(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username="pyjiro"))

    def test_正常系_データ確認(self):
        """初期状態でデータが1件登録されていることを確認"""
        self.assertEqual(Shop.objects.all().count(), 1)
        self.assertTrue(Shop.objects.filter(name="炎神").exists())

    def test_正常系_detail_pytaro(self):
        """詳細ページへ遷移できることをテスト"""
        self.pytaro_login()
        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, 200)
        # 該当データが登録されていることを確認
        self.assertTrue(detail_response.context["shop"], "炎神")

    def test_正常系_detail_未ログイン(self):
        """詳細ページへ遷移できることをテスト"""
        self.client.logout()
        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, 200)
        # 該当データが登録されていることを確認
        self.assertTrue(detail_response.context["shop"], "炎神")

    def test_正常系_update_pytaro(self):
        """記事編集ページへ遷移できることをテスト"""
        self.pytaro_login()
        update_response = self.client.get(self.update_url)
        self.assertEqual(update_response.status_code, 200)

    def test_異常系_update_pyjiro(self):
        """記事編集ページへ遷移できないことをテスト"""
        self.pyjiro_login()
        update_response = self.client.get(self.update_url)
        self.assertEqual(update_response.status_code, 403)

    def test_異常系_update_未ログイン(self):
        """記事編集ページへ遷移できないことをテスト"""
        self.client.logout()
        update_response = self.client.get(self.update_url)
        self.assertEqual(update_response.status_code, 403)
