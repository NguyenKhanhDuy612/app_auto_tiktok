from src.utils.database import db

user_collection = db["User"]

def get_user_by_quantity(quantity: int) -> list[dict]:
    """Lấy danh sách người dùng từ cơ sở dữ liệu dựa trên số lượng yêu cầu."""    
    users_cursor = user_collection.find({"Status": 0}, {"UserName": 1, "Password": 1}).limit(quantity)
    users = []
    for user in users_cursor:
        user["_id"] = str(user["_id"])  # Chuyển ObjectId thành chuỗi
        users.append(user)
    print(users)
    return users