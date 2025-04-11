import asyncio
import logging
import os
import random

from dotenv import load_dotenv
load_dotenv()

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async, StealthConfig
import pytest


async def open_tiktkok_login(page, username, password) -> None:
    """Đăng nhập vào TikTok với xử lý CAPTCHA."""
    await page.goto("https://www.tiktok.com/login/phone-or-email/email")
    await asyncio.sleep(5)

    # Nhập tên người dùng
    write_username = page.locator('xpath=//input[contains(@name,"username")]')
    await write_username.type(username)
    await asyncio.sleep(2)

    # Nhập mật khẩu
    write_password = page.get_by_placeholder('Password')
    await write_password.type(password)
    await asyncio.sleep(2)

    # Nhấn nút đăng nhập
    login_btn = await page.locator('//button[contains(@data-e2e,"login-button")]').click()
    await asyncio.sleep(5)

    print(f"✅ Đăng nhập thành công với tài khoản: {username}")


async def open_account(playwright, username, password, position):
    """Mở một trình duyệt và đăng nhập vào một tài khoản TikTok."""
    print(f"🚀 Đang mở trình duyệt cho tài khoản: {username} tại vị trí {position}")

    # Khởi chạy trình duyệt với kích thước cửa sổ nhỏ và vị trí cụ thể
    browser = await playwright.chromium.launch(
        headless=False,
        args=[
            f"--window-size=400,400",
            f"--window-position={position[0]},{position[1]}"
        ]
    )
    context = await browser.new_context(viewport={"width": 400, "height": 400})  # Đặt kích thước viewport
    page = await context.new_page()
    config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
    await stealth_async(page, config)

    # Đăng nhập TikTok
    await open_tiktkok_login(page, username, password)

    # Giữ trình duyệt mở
    print(f"✅ Trình duyệt cho tài khoản {username} đang mở tại vị trí {position}. Nhấn Ctrl+C để thoát.")
    await asyncio.sleep(10)  # Giữ trình duyệt mở trong 10 giây


async def open_multiple_accounts(accounts: list) -> None:
    """Mở đồng thời nhiều trình duyệt và đăng nhập vào các tài khoản TikTok."""
    async with async_playwright() as playwright:
        # Tọa độ khởi tạo cho các cửa sổ
        positions = [
            (x * 400, y * 400) for y in range(5) for x in range(10)
        ]  # Tạo 50 vị trí (10 hàng, 5 cột)
        tasks = [
            open_account(playwright, username, password, positions[i % len(positions)])
            for i, (username, password) in enumerate(accounts)
        ]
        await asyncio.gather(*tasks)  # Chạy đồng thời tất cả các tác vụ


@pytest.mark.asyncio
async def test_open_multiple_accounts(caplog):
    """Kiểm tra chức năng mở và đăng nhập nhiều tài khoản."""
    caplog.set_level(logging.DEBUG)

    # Danh sách tài khoản TikTok (username, password)
    accounts = [
        (f"username{i+1}", f"password{i+1}") for i in range(50)
    ]

    # Mở và đăng nhập nhiều tài khoản
    await open_multiple_accounts(accounts)


if __name__ == "__main__":
    # Nhập số lượng tài khoản cần mở
    try:
        num_accounts = 50 # Số lượng tài khoản mặc định

    except ValueError:
        print("❌ Vui lòng nhập một số hợp lệ.")
        exit(1)

    # Danh sách tài khoản TikTok (username, password)
    accounts = [
        (f"username{i+1}", f"password{i+1}") for i in range(50)
    ]

    # Kiểm tra số lượng tài khoản
    if num_accounts > len(accounts):
        print("❌ Số lượng tài khoản không đủ. Vui lòng thêm tài khoản vào danh sách.")
        exit(1)

    # Lấy danh sách tài khoản cần mở
    selected_accounts = accounts[:num_accounts]

    # Chạy chương trình
    asyncio.run(open_multiple_accounts(selected_accounts))