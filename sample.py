from playwright.sync_api import Playwright, expect, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:8000/main/")
    page.get_by_role("link", name="Login").click()
    page.get_by_placeholder("ユーザー名").click()
    page.get_by_placeholder("ユーザー名").fill("pytaro")
    page.get_by_placeholder("ユーザー名").press("Tab")
    page.get_by_placeholder("パスワード").fill("password")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("link", name="北京麻婆").click()
    page.frame_locator("#map").get_by_role("button", name="Zoom in").click()
    page.get_by_role("link", name="一覧").click()
    page.get_by_role("link", name="新しいお店").click()
    page.get_by_role("link", name="戻る").click()
    page.get_by_role("link", name="pytaroが登録したお店").click()
    page.get_by_role("link", name="編集").click()
    page.get_by_role("link", name="戻る").click()
    page.get_by_role("link", name="Logout").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
