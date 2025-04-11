from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.tiktok_captcha_solver.tests.new_object import test_join_livestream_and_comment

# Schemas
from src.schemas.watch_input import WatchInput

# models
from src.models.user_model import get_user_by_quantity
from src.models.hastag_model import getAllHasgtag

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cho phép origin của Next.js
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, v.v.)
    allow_headers=["*"],  # Cho phép tất cả header
)

class Item(BaseModel):
    name: str
    description: str

@app.post("/watch")
async def watch(input_data: WatchInput):
    try:
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
async def hastag():
    try:
        # Xử lý hastag ở đây
        result = getAllHasgtag()
        return {"message": f"Đã xử lý hastag", "result": result}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}