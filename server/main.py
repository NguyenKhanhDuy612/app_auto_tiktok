from fastapi import FastAPI
from pydantic import BaseModel
from src.tiktok_captcha_solver.tests.new_object import test_join_livestream_and_comment

# Schemas
from src.schemas.watch_input import WatchInput

# models
from src.models.user_model import get_user_by_quantity

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

@app.post("/watch")
async def watch(input_data: WatchInput):
    try:
        hastag = input_data.hastag
        users = input_data.users

        # Lấy danh sách người dùng từ database
        listUser = get_user_by_quantity(users)

        # Gán listUser vào input_data
        input_data.listUser = listUser

        # Truyền input_data vào hàm
        print("input_data:", input_data)
        await test_join_livestream_and_comment(input_data)
        return {"message": "chương trình đã hoàn thành!!!"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

@app.get("/hastag")
async def hastag(hastag: str):
    try:
        # Xử lý hastag ở đây
        return {"message": f"Đã xử lý hastag: {hastag}"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}