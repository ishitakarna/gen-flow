from fastapi import APIRouter
from crud import test_crud
from database.mysql import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(
    prefix="/test",
    tags=["test"]
)

@router.get("/users")
async def get_users_test(db: Session = Depends(get_db)):
    return test_crud.get_users_test(db=db)

@router.get("/workflows")
async def get_workflows_test(db: Session = Depends(get_db)):
    return test_crud.get_users_test(db=db)

