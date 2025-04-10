from pydantic import BaseModel

# Định nghĩa model cho object đầu vào
class WatchInput(BaseModel):
    url: str
    time: int
    comment: list[str]
    like: bool
    hastag: str
    users: int