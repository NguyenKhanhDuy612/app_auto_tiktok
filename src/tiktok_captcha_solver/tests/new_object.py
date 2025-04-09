import asyncio
import logging
import os
import requests

from dotenv import load_dotenv
load_dotenv()

from playwright.async_api import Page, async_playwright, expect
from playwright_stealth import stealth_async, StealthConfig
import pytest

from tiktok_captcha_solver.captchatype import CaptchaType
from ..asyncplaywrightsolver import AsyncPlaywrightSolver


async def open_tiktkok_login(page: Page) -> None:
    """Đăng nhập vào TikTok với xử lý CAPTCHA."""
    await page.goto("https://www.tiktok.com/login/phone-or-email/email")
    await asyncio.sleep(5)

    # Nhập tên người dùng
    write_username = page.locator('xpath=//input[contains(@name,"username")]')
    await write_username.type(os.environ["TIKTOK_USERNAME"])
    await asyncio.sleep(2)

    # Nhập mật khẩu
    write_password = page.get_by_placeholder('Password')
    await write_password.type(os.environ["TIKTOK_PASSWORD"])
    await asyncio.sleep(2)

    # Nhấn nút đăng nhập
    login_btn = await page.locator('//button[contains(@data-e2e,"login-button")]').click()
    await asyncio.sleep(5)

    # Xử lý CAPTCHA nếu xuất hiện
    # sadcaptcha = AsyncPlaywrightSolver(page, os.environ["API_KEY"])
    # await sadcaptcha.solve_captcha_if_present()
    print("✅ CAPTCHA đã được xử lý (nếu có).")

    await asyncio.sleep(10)


async def join_livestream_and_comment(page: Page, comment: str) -> None:
    """Tham gia livestream và gửi bình luận."""
    # Truy cập livestream
    await page.goto("https://www.tiktok.com/@batabilliards16/live")
    await asyncio.sleep(10)

    # Tìm ô nhập bình luận và thực hiện hover, click, rồi nhập
    comment_box = page.locator('.tiktok-1772j3i[contenteditable="plaintext-only"]')
    await comment_box.hover()  # Hover vào ô nhập bình luận
    await asyncio.sleep(1)
    await comment_box.click()  # Nhấn vào ô nhập bình luận
    await asyncio.sleep(1)
    await comment_box.fill(comment)  # Điền nội dung bình luận
    await asyncio.sleep(1)

    # Nhấn nút gửi bình luận
    send_button = page.locator('.tiktok-mortok.e2lzvyu9')  # Class của nút gửi
    await send_button.hover()  # Hover vào nút gửi
    await asyncio.sleep(1)
    await send_button.click()  # Nhấn nút gửi
    await asyncio.sleep(2)

    # Đảm bảo bình luận đã được gửi
    confirmation = page.locator('.tiktok-fa6jvh.e1tv929b2')  # Class xác nhận bình luận đã gửi
    if await confirmation.is_visible():
        print(f"✅ Đã gửi bình luận: {comment}")
    else:
        print("❌ Không thể gửi bình luận. Vui lòng kiểm tra lại.")


@pytest.mark.asyncio
async def test_join_livestream_and_comment(caplog):
    """Kiểm tra chức năng tham gia livestream và gửi bình luận."""
    caplog.set_level(logging.DEBUG)

    async with async_playwright() as p:
        # Khởi chạy trình duyệt
        browser = await p.chromium.launch(
            headless=False,
        )
        page = await browser.new_page()
        config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
        await stealth_async(page, config)

        # Đăng nhập TikTok
        await open_tiktkok_login(page)

        # Tham gia livestream và gửi bình luận
        comment = "Hello Hoang"
        await join_livestream_and_comment(page, comment)

        # Giữ trình duyệt mở
        print("✅ Trình duyệt vẫn đang mở. Nhấn Ctrl+C để thoát.")

        # Chờ vô hạn để giữ trình duyệt mở
        await asyncio.Future()  # Chờ vô hạn

if __name__ == "__main__":
    # Chạy kiểm tra thủ công
    asyncio.run(test_join_livestream_and_comment(logging.getLogger()))