import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

try: 
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["MarketingTool01"]
    print("Kết nối thành công!")
except Exception as e:
    print(f"Lỗi kết nối: {e}")