from fastapi import APIRouter, Form
from ..database.mysql import get_db
from ..crud import user_crud
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# TODO: hash password
@router.post("/login")
async def get_user_login(db: Session = Depends(get_db), email: str = Form(), passwd: str = Form()):
    return user_crud.verify_login(db=db,emailAddress=email, pwdHash=passwd)