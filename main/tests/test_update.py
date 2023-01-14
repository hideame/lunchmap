from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from main.models import Category, Shop


class TestUpdateView(TestCase):
    fixtures = ["users", "category"]
    detail_url = reverse_lazy("main:detail", kwargs={"pk": 1})
    update_url = reverse_lazy("main:update", kwargs={"pk": 1})
    char_255 = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjkkkkkkkkkkllllllllllmmmmmmmmmmnnnnnnnnnnooooooooooppppppppppqqqqqqqqqqrrrrrrrrrrssssssssssttttttttttuuuuuuuuuuvvvvvvvvvvwwwwwwwwwwxxxxxxxxxxyyyyyyyyyyzzzzz"

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

    def test_正常系_update_pytaro(self):
        self.pytaro_login()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "アグニ",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        update_response = self.client.post(self.update_url, params)
        # 正常終了を確認
        self.assertRedirects(
            update_response,
            self.detail_url,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        detail_response = self.client.get(self.detail_url)
        # アグニに変更されていることを確認
        self.assertTrue(Shop.objects.filter(name="アグニ").exists())
        self.assertTrue(detail_response.context["shop"], "アグニ")

    def test_異常系_update_pyjiro(self):
        self.pyjiro_login()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "アグニ",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        update_response = self.client.post(self.update_url, params)
        # 403エラーを確認
        self.assertEqual(update_response.status_code, 403)
        detail_response = self.client.get(self.detail_url)
        # データが変更できていないことを確認
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())

    def test_異常系_update_未ログイン(self):
        self.client.logout()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "アグニ",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        update_response = self.client.post(self.update_url, params)
        # 403エラーを確認
        self.assertEqual(update_response.status_code, 403)
        detail_response = self.client.get(self.detail_url)
        # データが変更できていないことを確認
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())

    def test_異常系_update_店名なし(self):
        self.pytaro_login()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        update_response = self.client.post(self.update_url, params)
        # エラーとなることを確認
        self.assertNotEqual(update_response.status_code, 302)
        expect_form_errors = {"name": ["このフィールドは必須です。"]}
        self.assertDictEqual(update_response.context["form"].errors, expect_form_errors)

    def test_異常系_update_住所なし(self):
        self.pytaro_login()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "炎神",
            "address": "",
            "category": category.id,
        }
        update_response = self.client.post(self.update_url, params)
        # エラーとなることを確認
        self.assertNotEqual(update_response.status_code, 302)
        expect_form_errors = {"address": ["このフィールドは必須です。"]}
        self.assertDictEqual(update_response.context["form"].errors, expect_form_errors)

    def test_異常系_update_カテゴリなし(self):
        self.pytaro_login()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        params = {
            "name": "炎神",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": "",
        }
        update_response = self.client.post(self.update_url, params)
        # エラーとなることを確認
        self.assertNotEqual(update_response.status_code, 302)
        expect_form_errors = {"category": ["このフィールドは必須です。"]}
        self.assertDictEqual(update_response.context["form"].errors, expect_form_errors)

    def test_異常系_update_存在しないカテゴリID(self):
        self.pytaro_login()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        category = Category.objects.get(name="中華料理")
        category.id = 99  # 存在しないカテゴリID
        params = {
            "name": "炎神",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        update_response = self.client.post(self.update_url, params)
        # エラーとなることを確認
        self.assertNotEqual(update_response.status_code, 302)
        expect_form_errors = {"category": ["正しく選択してください。選択したものは候補にありません。"]}
        self.assertDictEqual(update_response.context["form"].errors, expect_form_errors)

    def test_正常系_update_店名255文字(self):
        self.pytaro_login()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        category = Category.objects.get(name="中華料理")
        params = {
            "name": self.char_255,
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        update_response = self.client.post(self.update_url, params)
        # 正常終了を確認
        self.assertRedirects(
            update_response,
            self.detail_url,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        detail_response = self.client.get(self.detail_url)
        # 店名が変更されていることを確認
        self.assertTrue(Shop.objects.filter(name=self.char_255).exists())
        self.assertTrue(detail_response.context["shop"], self.char_255)

    def test_異常系_update_店名256文字(self):
        self.pytaro_login()
        # 炎神が登録されていることを確認
        detail_response = self.client.get(self.detail_url)
        self.assertTrue(detail_response.context["shop"], "炎神")
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        # データの編集
        category = Category.objects.get(name="中華料理")
        params = {
            "name": self.char_255 + "a",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        update_response = self.client.post(self.update_url, params)
        # エラーとなることを確認
        self.assertNotEqual(update_response.status_code, 302)
        expect_form_errors = {"name": ["この値は 255 文字以下でなければなりません( 256 文字になっています)。"]}
        self.assertDictEqual(update_response.context["form"].errors, expect_form_errors)
        # 店名が変更できていないことを確認
        self.assertFalse(Shop.objects.filter(name=f"{self.char_255}a").exists())
