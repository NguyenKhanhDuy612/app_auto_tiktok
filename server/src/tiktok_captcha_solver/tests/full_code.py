import asyncio
import logging
import os
import requests

from dotenv import load_dotenv
from playwright.async_api import Page, async_playwright, expect
from playwright_stealth import stealth_async, StealthConfig
import pytest

from tiktok_captcha_solver.captchatype import CaptchaType
from ..asyncplaywrightsolver import AsyncPlaywrightSolver

load_dotenv()

# Proxy-related functions
def get_proxy_list():
    print("🔄 Đang lấy danh sách proxy...")
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    response = requests.get(url)
    proxy_list = response.text.strip().split('\n')
    print(f"✅ Đã lấy được {len(proxy_list)} proxy.")
    return proxy_list

def test_proxy(proxy):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        if r.status_code == 200:
            return True
    except Exception:
        pass
    return False

async def open_tiktkok_login(page: Page) -> None:
    await page.goto("https://www.tiktok.com/login/phone-or-email/email")
    await asyncio.sleep(10)
    write_username = page.locator('xpath=//input[contains(@name,"username")]')
    await write_username.type(os.environ["TIKTOK_USERNAME"])
    await asyncio.sleep(2)
    write_password = page.get_by_placeholder('Password')
    await write_password.type(os.environ["TIKTOK_PASSWORD"])
    await asyncio.sleep(2)
    login_btn = await page.locator('//button[contains(@data-e2e,"login-button")]').click()
    await asyncio.sleep(10)

@pytest.mark.asyncio
async def test_solve_captcha_at_login_with_proxy(caplog):
    caplog.set_level(logging.DEBUG)

    # Get proxy list and find a working proxy
    proxy_list = get_proxy_list()
    working_proxy = None
    for proxy in proxy_list:
        proxy = proxy.strip()
        print(f"🧪 Đang thử proxy: {proxy}...", end=" ")
        if test_proxy(proxy):
            print("✅ Thành công! Dùng được proxy.")
            working_proxy = proxy
            break
        else:
            print("❌ Không dùng được.")

    if not working_proxy:
        print("🚫 Không tìm thấy proxy nào hoạt động.")
        return

    # Use Playwright with the working proxy
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            proxy={
                "server": f"http://{working_proxy}"
            }
        )
        page = await browser.new_page()
        config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
        await stealth_async(page, config)
        await open_tiktkok_login(page)
        sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
        await sadcaptcha.solve_captcha_if_present()
        await expect(page.locator("css=#header-more-menu-icon")).to_be_visible(timeout=30000)

if __name__ == "__main__":
    # Run the test manually if needed
    asyncio.run(test_solve_captcha_at_login_with_proxy(logging.getLogger()))