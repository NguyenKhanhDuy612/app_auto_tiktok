from src.utils.database import db

proxy_collection = db["Hashtag"]

def getAllHasgtag() -> list[dict]:
    """Lấy tất cả hashtag từ cơ sở dữ liệu."""
    hashtags_cursor = proxy_collection.find({}, {"Status": 0, "IsDeleted": 0})
    hashtags = []
    for hashtag in hashtags_cursor:
        hashtag["_id"] = str(hashtag["_id"])  # Chuyển ObjectId thành chuỗi
        hashtags.append(hashtag)
    return hashtags