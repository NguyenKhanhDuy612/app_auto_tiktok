import requests
import asyncio
from playwright.sync_api import sync_playwright

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
        return r.status_code == 200
    except:
        return False

def open_browser_with_proxy(proxy):
    with sync_playwright() as p:
        browser = p.chromium.launch(proxy={"server": f"http://{proxy}"}, headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://httpbin.org/ip")
        print("✅ Trình duyệt đã mở. Nhấn Ctrl+C để thoát.")
        input("⏸ Nhấn Enter để đóng...")
        browser.close()

def main():
    proxy_list = get_proxy_list()

    for proxy in proxy_list:
        proxy = proxy.strip()
        print(f"🧪 Đang thử proxy: {proxy}...", end=" ")

        if test_proxy(proxy):
            print("✅ Hoạt động!")
            open_browser_with_proxy(proxy)
            break
        else:
            print("❌ Không dùng được.")

if __name__ == "__main__":
    main()
