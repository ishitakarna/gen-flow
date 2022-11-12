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

@router.get("/userLogin")
async def get_user_login(db: Session = Depends(get_db)):
    return test_crud.verify_login(db=db,emailAddress='samarthgupta@gmail.com', pwdHash="abcd123")

@router.get("/userDeptProcesses")
async def get_all_processes_for_a_department(db: Session = Depends(get_db)):
    return test_crud.get_all_processes_for_a_department(db=db,emailAddress='bkulka@gmail.com')

@router.get("/workflow/addInstance")
async def add_workflow_instance(db: Session = Depends(get_db)):
    return test_crud.add_workflow_instance(db=db,wfId=100)

@router.get("/workflow/deleteInstance")
async def delete_workflow_instance(db: Session = Depends(get_db)):
    return test_crud.delete_workflow_instance(db=db,wfInstanceId=100)

@router.get("/process/completeInstance")
async def complete_process_instance(db: Session = Depends(get_db)):
    return test_crud.complete_process_instance(db=db,processInstanceId=100, params={})