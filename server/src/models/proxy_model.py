from src.utils.database import db

proxy_collection = db["Proxy"]

def verify_proxy_db(proxy: str) -> list[dict]:
    try:
        """Kiểm tra proxy trong cơ sở dữ liệu."""
        proxy_cursor = proxy_collection.find_one({"proxy": proxy})
        print(proxy_cursor)
        if proxy_cursor:
            proxy_cursor["_id"] = str(proxy_cursor["_id"])  # Chuyển ObjectId thành chuỗi
            return True
        else:
            """Lưu proxy vào cơ sở dữ liệu."""
            # Tạo tài liệu proxy
            proxy_data = {"proxy": proxy}
            
            # Lưu vào database
            result = proxy_collection.insert_one(proxy_data)
            
            # Trả về thông tin proxy đã lưu
            return False
    except Exception as e:
        # Xử lý lỗi khi lưu vào database
        print(f"Lỗi khi lưu proxy {proxy} vào cơ sở dữ liệu: {e}")
        return False
    