import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

def open_chrome_with_proxy(proxy):
    print(f"🚀 Đang mở Chrome qua proxy: {proxy}")
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("http://httpbin.org/ip")  # Kiểm tra IP hiện tại
    return driver

def main():
    proxy_list = get_proxy_list()

    print("🔍 Đang kiểm tra proxy hoạt động...")
    for proxy in proxy_list:
        proxy = proxy.strip()
        print(f"🧪 Đang thử proxy: {proxy}...", end=" ")

        if test_proxy(proxy):
            print("✅ Thành công! Dùng được proxy.")
            driver = open_chrome_with_proxy(proxy)
            input("🔎 Chrome đã mở. Nhấn Enter để đóng lại...")
            driver.quit()
            break
        else:
            print("❌ Không dùng được.")

    else:
        print("🚫 Không tìm thấy proxy nào hoạt động.")

if __name__ == "__main__":
    main()
