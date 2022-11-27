from fastapi import APIRouter, Form
from database.mysql import get_db
from crud import user_crud
from sqlalchemy.orm import Session
from fastapi import Depends
from pydantic import BaseModel

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

class UserLogin(BaseModel):
    email: str
    passwd: str

# TODO: hash password
@router.post("/login")
async def get_user_login(userData: UserLogin, db: Session = Depends(get_db)):
    return user_crud.verify_login(db=db,emailAddress=userData.email, pwdHash=userData.passwd)