from pydantic import BaseModel
from typing import Optional, List

#Định nghĩa model cho user
class UserInput(BaseModel):
    username: str
    password: str

# Định nghĩa model cho object đầu vào
class WatchInput(BaseModel):
    url: str
    time: int
    comment: list[str]
    like: bool
    hastag: str
    users: int
    listUser: Optional[List[dict]] = None  # Thêm field listUser

