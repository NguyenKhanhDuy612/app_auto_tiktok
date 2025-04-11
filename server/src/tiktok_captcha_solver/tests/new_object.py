import asyncio
import logging
import os
import random
import time
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ..seleniumsolver import SeleniumSolver

from src.models.proxy_model import verify_proxy_db
from src.schemas.watch_input import WatchInput

load_dotenv()


def open_tiktok_login(driver, username, password) -> None:
    """Đăng nhập vào TikTok."""
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(15)

    # Nhập tên người dùng
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        username_input.send_keys(username)
        time.sleep(2)
    except Exception as e:
        print(f"⚠️ Lỗi khi nhập tên người dùng: {e}")
        return

    # Nhập mật khẩu
    try:
        password_input = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
        password_input.send_keys(password)
        time.sleep(2)
    except Exception as e:
        print(f"⚠️ Lỗi khi nhập mật khẩu: {e}")
        return

    # Nhấn nút đăng nhập
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-e2e,"login-button")]'))
        )
        login_button.click()
        time.sleep(20)
        print("✅ Đã cố gắng đăng nhập.")
    except Exception as e:
        print(f"⚠️ Lỗi khi nhấn nút đăng nhập: {e}")
        return
    
    #captcha
    try:
        sadcaptcha = SeleniumSolver(driver, os.environ["API_KEY"], mouse_step_size=2)
        sadcaptcha.solve_captcha_if_present()
        print("✅ CAPTCHA đã được xử lý (nếu có).")
    except Exception as e:
        print(f"⚠️ Lỗi khi xử lý CAPTCHA: {e}")
        return


    # await asyncio.sleep(10)
    time.sleep(10)

def join_livestream_and_comment(driver, comments: list[str], num_comments: int, like: bool,urlVideo: str) -> None:
    """Tham gia livestream và gửi bình luận."""
    try:
        driver.get(urlVideo)
        time.sleep(10)

        for i in range(num_comments):
            try:
                random_comment = random.choice(comments)
                print(f"📝 Đang chuẩn bị bình luận {i + 1}/{num_comments}: {random_comment}")
                time.sleep(15)

                # Tìm ô nhập bình luận
                comment_box = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="plaintext-only"]'))
                )
                print("✅ Đã tìm thấy ô bình luận.")
                comment_box.click()
                time.sleep(1)
                comment_box.send_keys(random_comment)
                time.sleep(1)

                # Nhấn nút gửi
                send_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class*="tiktok-"] button[type="submit"]'))
                )
                send_button.click()
                print(f"✅ Bình luận {i + 1}/{num_comments} đã gửi: {random_comment}")
                time.sleep(2)

                # Thả tim nếu bật
                if like:
                    try:
                        heart_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '.tiktok-1cu4ad.e1tv929b3'))
                        )
                        heart_button.click()
                        print(f"❤️ Đã thả tim sau bình luận {i + 1}")
                    except Exception as e:
                        print(f"⚠️ Không tìm thấy hoặc không thể click nút thả tim: {e}")

            except Exception as e:
                print(f"❌ Lỗi khi gửi bình luận {i + 1}: {e}")

        print("🎉 Hoàn thành việc gửi bình luận!")

    except Exception as e:
        print(f"⚠️ Lỗi khi tham gia livestream: {e}")


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
        r_http = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        r_https = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
        if r_http.status_code == 200 and r_https.status_code == 200:
            return True
    except Exception:
        pass
    return False

async def test_join_livestream_and_comment(input_data: WatchInput):
    """Kiểm tra chức năng tham gia livestream và gửi bình luận."""
    proxy_list = get_proxy_list()
    print(f"Số lượng proxy: {len(proxy_list)}")
    working_proxy = None

    for proxy in proxy_list:
        proxy = proxy.strip()
        # Kiểm tra proxy trong cơ sở dữ liệu
        print(f"🧪 Đang thử proxy: {proxy}...", end=" ")
        if test_proxy(proxy):
            proxy_db = verify_proxy_db(proxy)
            if proxy_db:
                print("✅ Proxy đã được lưu vào cơ sở dữ liệu.")
                print("✅ Thành công! Dùng được proxy.")
                working_proxy = proxy
                break
        else:
            print("❌ Không dùng được.")

    if working_proxy:
        print(f"🧪 Đang thử mở trình duyệt với proxy: {working_proxy}...")
        try:
            chrome_options = Options()
            chrome_options.add_argument(f'--proxy-server=http://{working_proxy}')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            driver = webdriver.Chrome(options=chrome_options)
            driver.set_window_size(1200, 800)

            username = input_data.listUser[0]["UserName"]  # Assuming you want to use the first user
            password = input_data.listUser[0]["Password"]  # Assuming you want to use the first user

            # Đăng nhập TikTok
            open_tiktok_login(driver, username, password)

            # Danh sách bình luận
            comments = input_data.comment
            num_comments = len(comments)
            like = input_data.like
            urlVideo = input_data.url
            print(f"Số lượng bình luận: {num_comments}")
            print(f"Thả tim: {'Bật' if like else 'Tắt'}")

            # Tham gia livestream và gửi bình luận
            join_livestream_and_comment(driver, comments, num_comments, like,urlVideo)

            # Giữ trình duyệt mở
            print("✅ Trình duyệt vẫn đang mở. Nhấn Ctrl+C để thoát.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🔒 Đã nhận lệnh dừng. Đang đóng trình duyệt...")
            finally:
                driver.quit()
                print("🔒 Đã đóng trình duyệt.")

        except Exception as e:
            print(f"⚠️ Lỗi khi khởi tạo hoặc sử dụng trình duyệt: {e}")
        finally:
            if 'driver' in locals() and driver:
                driver.quit()
                print("🔒 Đảm bảo trình duyệt đã đóng.")
    else:
        print("🚫 Không thể mở trình duyệt vì không tìm thấy proxy hoạt động.")


if __name__ == "__main__":
    # Ví dụ dữ liệu đầu vào (thay thế bằng dữ liệu thực tế của bạn)
    test_input_data = WatchInput(
        listUser=[
            {"UserName": os.environ.get("TIKTOK_USERNAME", "testuser"), "Password": os.environ.get("TIKTOK_PASSWORD", "testpass")},
            {"UserName": "user2", "Password": "pass2"},
            {"UserName": "user3", "Password": "pass3"},
        ],
        comment=["Bình luận 1", "Bình luận 2", "Bình luận 3"],
        like=True,
    )
    asyncio.run(test_join_livestream_and_comment(test_input_data))