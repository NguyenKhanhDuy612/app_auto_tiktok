import asyncio
import datetime
import logging
import os
import random
import threading
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
    # username = os.environ.get("TIKTOK_USERNAME", username)
    """Đăng nhập vào TikTok."""
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(10)

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
        login_button = driver.find_element(By.XPATH, '//button[contains(@data-e2e,"login-button")]')
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

def like_continuously(driver, watch_until: datetime.datetime):
    while datetime.datetime.now() < watch_until:
        try:
            heart_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.tiktok-1cu4ad.e1tv929b3'))
            )
            heart_button.click()
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❤️ Đã thả tim.")
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⚠️ Không thể thả tim: {e}")
        time.sleep(10)  # Cách nhau 10 giây mỗi lần tym

def comment_on_livestream(driver, comments: list[str], num_comments: int):
    for i in range(num_comments):
        try:
            random_comment = random.choice(comments)
            print(f"📝 Đang chuẩn bị bình luận {i + 1}/{num_comments}: {random_comment}")
            time.sleep(15)

            comment_box = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="plaintext-only"]'))
            )
            print("✅ Đã tìm thấy ô bình luận.")
            comment_box.click()
            time.sleep(1)
            comment_box.send_keys(random_comment)
            time.sleep(1)

            send_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.e2lzvyu9'))
            )
            send_button.click()
            print(f"✅ Bình luận {i + 1}/{num_comments} đã gửi: {random_comment}")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Lỗi khi gửi bình luận {i + 1}: {e}")

def join_livestream_and_comment(driver, comments: list[str], num_comments: int, like: bool,urlVideo: str, timelogout: int) -> None:
    """Tham gia livestream và gửi bình luận."""
    try:
        driver.get(urlVideo)
        time.sleep(10)
        start_watch_time = datetime.datetime.now()
        watch_until = start_watch_time + datetime.timedelta(minutes=timelogout)

        # Bắt đầu thread thả tym nếu like = True
        if like:
            like_thread = threading.Thread(target=like_continuously, args=(driver, watch_until))
            like_thread.start()

        # Bắt đầu bình luận (trong thread chính)
        comment_on_livestream(driver, comments, num_comments)

        # Hiển thị thời gian xem live còn lại
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⏳ Đang xem live đến {watch_until.strftime('%H:%M:%S')}.")
        while datetime.datetime.now() < watch_until:
            remaining_time = watch_until - datetime.datetime.now()
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⏳ Còn lại: {remaining_time.seconds} giây.", end='\r')
            time.sleep(5)

        # Kết thúc
        print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] 🎬 Hết thời gian xem live.")
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🔄 Cuộn màn hình để xem live khác...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(5)

        print("🚪 Đang đóng trình duyệt.")
        driver.quit()
        print("🔒 Đã đóng trình duyệt.")

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

def run_watch_task(user_data: dict, comments: list[str], like: bool, urlVideo: str, timelogout: int):
    """Chạy một phiên đăng nhập và bình luận cho 1 tài khoản TikTok."""
    proxy_list = get_proxy_list()
    working_proxy = None

    for proxy in proxy_list:
        proxy = proxy.strip()
        print(f"🧪 Đang thử proxy: {proxy}...", end=" ")
        if test_proxy(proxy):
            proxy_db = verify_proxy_db(proxy)
            if proxy_db:
                print("✅ Thành công! Dùng được proxy.")
                working_proxy = proxy
                break
        else:
            print("❌ Không dùng được.")

    if working_proxy:
        try:
            chrome_options = Options()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument(f'--proxy-server=http://{working_proxy}')

            driver = webdriver.Chrome(options=chrome_options)
            driver.set_window_size(1200, 800)

            username = user_data["UserName"]
            password = user_data["Password"]
            print(f"🔐 Bắt đầu với user: {username}")

            open_tiktok_login(driver, username, password)
            join_livestream_and_comment(driver, comments, len(comments), like, urlVideo, timelogout)

        except Exception as e:
            print(f"❌ Lỗi với user {user_data['UserName']}: {e}")
        finally:
            if 'driver' in locals():
                driver.quit()
    else:
        print(f"🚫 User {user_data['UserName']} không tìm thấy proxy hoạt động.")


async def test_join_livestream_and_comment(input_data: WatchInput):
    tasks = []

    for user in input_data.listUser:
        task = asyncio.to_thread(
            run_watch_task,
            user,
            input_data.comment,
            input_data.like,
            input_data.url,
            input_data.time
        )
        tasks.append(task)

    await asyncio.gather(*tasks)

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
