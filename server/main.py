from fastapi import FastAPI
from src.utils.database import collection
from pydantic import BaseModel
from bson.objectid import ObjectId
from src.tiktok_captcha_solver.tests.new_object import test_join_livestream_and_comment
from src.schemas.watch_input import WatchInput

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

@app.post("/watch")
async def watch(input_data: WatchInput):
    try:
        hastag = input_data.hastag
        users = input_data.users

        print(f"Hashtag: {hastag}")
        print(f"Users: {users}")

        for i in range(users):
            # Lưu vào database
            result = collection.insert_one(input_data.dict())
            print(f"Inserted ID: {result.inserted_id}")
        # await test_join_livestream_and_comment(input_data)
        return {"message": "chương trình đã hoàn thành!!!"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}
        

# @app.post("/items")
# def create_item(item: Item):
#     result = collection.insert_one(item.dict())
#     return {"id": str(result.inserted_id)}

@app.get("/items")
def get_items():
    items = []
    for item in collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items
