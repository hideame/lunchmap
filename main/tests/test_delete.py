from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from main.models import Category, Shop


class TestDeleteView(TestCase):
    fixtures = ["users", "category"]
    list_url = reverse_lazy("main:list")
    detail_url = reverse_lazy("main:detail", kwargs={"pk": 1})
    delete_url = reverse_lazy("main:delete", kwargs={"pk": 1})

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

    def test_正常系_delete_pytaro(self):
        self.pytaro_login()
        # 炎神が登録されていることを確認
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        list_response = self.client.get(self.list_url)
        self.assertTrue(list_response.context["shop_list"], "炎神")
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        # データの削除
        delete_response = self.client.post(self.delete_url)
        # 正常終了を確認
        self.assertRedirects(
            delete_response,
            self.list_url,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        list_response = self.client.get(self.list_url)
        # データが削除されていることを確認
        self.assertFalse(Shop.objects.filter(name="炎神").exists())
        self.assertFalse(list_response.context["shop_list"], "炎神")
        # 詳細ページが削除されたことを確認
        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, 404)

    def test_異常系_delete_pyjiro(self):
        self.pyjiro_login()
        # 炎神が登録されていることを確認
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        list_response = self.client.get(self.list_url)
        self.assertTrue(list_response.context["shop_list"], "炎神")
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        # データの削除
        delete_response = self.client.post(self.delete_url)
        # 403エラーを確認
        self.assertEqual(delete_response.status_code, 403)
        # データが削除できていないことを確認
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        self.assertTrue(list_response.context["shop_list"], "炎神")
        # 詳細ページが削除されていないことを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")

    def test_異常系_delete_未ログイン(self):
        self.client.logout()
        # 炎神が登録されていることを確認
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        list_response = self.client.get(self.list_url)
        self.assertTrue(list_response.context["shop_list"], "炎神")
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        # データの削除
        delete_response = self.client.post(self.delete_url)
        # 403エラーを確認
        self.assertEqual(delete_response.status_code, 403)
        # データが削除できていないことを確認
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        self.assertTrue(list_response.context["shop_list"], "炎神")
        # 詳細ページが削除されていないことを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
