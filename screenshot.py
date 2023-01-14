import datetime
import time

from playwright.sync_api import Playwright, expect, sync_playwright


def run(playwright: Playwright) -> None:
    # ブラウザをバックグラウンドで起動する場合（headless=True）
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    date = datetime.datetime.now().strftime("%Y%m%d")
    dir = f"visual_regression_test/{date}/"
    WAIT_SEC = 0.1
    WAIT_SEC_MAP = 0.5

    # login
    page.goto("http://127.0.0.1:8000/main/")
    page.get_by_role("link", name="Login").click()
    page.wait_for_load_state()
    time.sleep(WAIT_SEC)
    page.screenshot(path=dir + "login.png")
    # 本来はコマンドラインから渡す（※今回はスキップ）
    page.get_by_placeholder("ユーザー名").click()
    page.get_by_placeholder("ユーザー名").fill("pytaro")
    page.get_by_placeholder("パスワード").click()
    page.get_by_placeholder("パスワード").fill("password")
    page.get_by_role("button", name="Login").click()

    # list
    page.wait_for_load_state()
    time.sleep(WAIT_SEC)
    page.screenshot(path=dir + "list.png")

    # detail
    page.get_by_role("link", name="北京麻婆").click()
    page.frame_locator("#map").get_by_role("button", name="Zoom in").click()
    page.wait_for_load_state()
    time.sleep(WAIT_SEC_MAP)
    page.screenshot(path=dir + "detail.png")

    # create
    page.get_by_role("link", name="一覧").click()
    page.get_by_role("link", name="新しいお店").click()
    page.wait_for_load_state()
    time.sleep(WAIT_SEC)
    page.screenshot(path=dir + "create.png")

    # update
    page.get_by_role("link", name="戻る").click()
    page.get_by_role("link", name="pytaroが登録したお店").click()
    page.get_by_role("link", name="編集").click()
    page.wait_for_load_state()
    time.sleep(WAIT_SEC)
    page.screenshot(path=dir + "update.png")

    # logout
    page.get_by_role("link", name="戻る").click()
    page.get_by_role("link", name="Logout").click()
    page.wait_for_load_state()
    time.sleep(WAIT_SEC)
    page.screenshot(path=dir + "update.png")

    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
