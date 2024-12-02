from fastapi import FastAPI
from fastapi import HTTPException
from typing import List
from pydantic import BaseModel


app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


class UserCreate(BaseModel):
    username: str
    age: int


@app.get("/users", response_model=List[User])
async def get_users():
    return users


@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    new_id = max((ur.id for ur in users), default=0) + 1
    new_user = User(id=new_id,
                    username=user.username,
                    age=user.age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    for ur in users:
        if ur.id == user_id:
            ur.username = user.username
            ur.age = user.age
            return ur
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for i, ur in enumerate(users):
        if ur.id == user_id:
            del users[i]
            return ur
    raise HTTPException(status_code=404, detail="User was not found")
