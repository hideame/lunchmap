from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from main.models import Category, Shop


class TestCreateView(TestCase):
    fixtures = ["users", "category"]
    list_url = reverse_lazy("main:list")
    create_url = reverse_lazy("main:create")
    detail_url = reverse_lazy("main:detail", kwargs={"pk": 1})
    char_255 = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjkkkkkkkkkkllllllllllmmmmmmmmmmnnnnnnnnnnooooooooooppppppppppqqqqqqqqqqrrrrrrrrrrssssssssssttttttttttuuuuuuuuuuvvvvvvvvvvwwwwwwwwwwxxxxxxxxxxyyyyyyyyyyzzzzz"

    def pytaro_login(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username="pytaro"))

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

    def test_正常系_create_pytaro(self):
        self.pytaro_login()
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "炎神",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(name="炎神").exists())
        # データの登録
        create_response = self.client.post(self.create_url, params)
        self.assertRedirects(
            create_response,
            self.detail_url,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        detail_response = self.client.get(self.detail_url)
        # データが登録されていることを確認
        self.assertTrue(Shop.objects.filter(name="炎神").exists())
        self.assertTrue(detail_response.context["shop"], "炎神")

    def test_異常系_create_未ログイン(self):
        self.client.logout()
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "炎神",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(name="炎神").exists())
        # データの登録
        create_response = self.client.post(self.create_url, params)
        expected_url = "/accounts/login/?next=/main/create/"
        self.assertRedirects(
            create_response,
            expected_url,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(name="炎神").exists())

    def test_異常系_create_店名なし(self):
        self.pytaro_login()
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(address="茨城県水戸市桜川2-1-6アイランドビル1F").exists())
        # データの登録
        create_response = self.client.post(self.create_url, params)
        self.assertNotEqual(create_response.status_code, 302)
        expect_form_errors = {"name": ["このフィールドは必須です。"]}
        self.assertDictEqual(create_response.context["form"].errors, expect_form_errors)

    def test_異常系_create_住所なし(self):
        self.pytaro_login()
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "炎神",
            "address": "",
            "category": category.id,
        }
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(name="炎神").exists())
        # データの登録
        create_response = self.client.post(self.create_url, params)
        self.assertNotEqual(create_response.status_code, 302)
        expect_form_errors = {"address": ["このフィールドは必須です。"]}
        self.assertDictEqual(create_response.context["form"].errors, expect_form_errors)

    def test_異常系_create_カテゴリなし(self):
        self.pytaro_login()
        category = Category.objects.get(name="中華料理")
        params = {
            "name": "炎神",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": "",
        }
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(name="炎神").exists())
        # データの登録
        create_response = self.client.post(self.create_url, params)
        self.assertNotEqual(create_response.status_code, 302)
        expect_form_errors = {"category": ["このフィールドは必須です。"]}
        self.assertDictEqual(create_response.context["form"].errors, expect_form_errors)

    def test_異常系_create_存在しないカテゴリID(self):
        self.pytaro_login()
        category = Category.objects.get(name="中華料理")
        category.id = 99  # 存在しないカテゴリID
        params = {
            "name": "炎神",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(name="炎神").exists())
        # データの登録
        create_response = self.client.post(self.create_url, params)
        self.assertNotEqual(create_response.status_code, 302)
        expect_form_errors = {"category": ["正しく選択してください。選択したものは候補にありません。"]}
        self.assertDictEqual(create_response.context["form"].errors, expect_form_errors)

    def test_正常系_create_店名255文字(self):
        self.pytaro_login()
        category = Category.objects.get(name="中華料理")
        params = {
            "name": self.char_255,
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(address="茨城県水戸市桜川2-1-6アイランドビル1F").exists())
        # データの登録
        create_response = self.client.post(self.create_url, params)
        self.assertRedirects(
            create_response,
            self.detail_url,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        detail_response = self.client.get(self.detail_url)
        # データが登録されていることを確認
        self.assertTrue(Shop.objects.filter(address="茨城県水戸市桜川2-1-6アイランドビル1F").exists())
        self.assertTrue(Shop.objects.filter(name=self.char_255).exists())
        self.assertTrue(detail_response.context["shop"], self.char_255)

    def test_異常系_create_店名256文字(self):
        self.pytaro_login()
        category = Category.objects.get(name="中華料理")
        params = {
            "name": self.char_255 + "a",
            "address": "茨城県水戸市桜川2-1-6アイランドビル1F",
            "category": category.id,
        }
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(address="茨城県水戸市桜川2-1-6アイランドビル1F").exists())
        # データの登録
        create_response = self.client.post(self.create_url, params)
        self.assertNotEqual(create_response.status_code, 302)
        expect_form_errors = {"name": ["この値は 255 文字以下でなければなりません( 256 文字になっています)。"]}
        self.assertDictEqual(create_response.context["form"].errors, expect_form_errors)
        # データが登録されていないことを確認
        self.assertFalse(Shop.objects.filter(address="茨城県水戸市桜川2-1-6アイランドビル1F").exists())
