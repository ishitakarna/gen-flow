from fastapi import APIRouter, Form
from ..database.mysql import get_db
from ..crud import process_crud
from sqlalchemy.orm import Session
from fastapi import Depends
from pydantic import BaseModel

router = APIRouter(     
    prefix="/process",
    tags=["process"]
)

class CompleteProcess(BaseModel):
    processInstanceId: int
    wfInstanceId: int
    processId: int

    # 4892
    # 930
    # 11

@router.get("/parameters/{processId}")
async def get_params_for_process_completion(processId: int, db: Session = Depends(get_db)):
    return process_crud.get_params_for_process_completion(db, processId=processId)

@router.post("/complete")
async def complete_process_instance(completeProcessObj: CompleteProcess, db: Session = Depends(get_db)):
    print('hehe')
    # Input - parameters required for the process type
    # Check if this is the last process - if yes then complete the workflow instance as well
    # If not, then complete and update the process instance, update the workflow instance and start the next process
    return process_crud.complete_process(processInstanceId=completeProcessObj.processInstanceId, wfInstanceId=completeProcessObj.wfInstanceId, processId=completeProcessObj.processId, processParamInstances=None, db=db)


