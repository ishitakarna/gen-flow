from fastapi import APIRouter, Form
from database.mysql import get_db
from crud import process_crud
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from pydantic import BaseModel

router = APIRouter(     
    prefix="/process",
    tags=["process"]
)

class ProcessParamInstanceObject(BaseModel):
    paramVal: str
    processInstanceId: int
    paramId: int

class CompleteProcess(BaseModel):
    processInstanceId: int
    seqNumber: int
    wfId: int
    wfInstanceId: int
    params: List[ProcessParamInstanceObject]

@router.get("/parameters/{processId}")
async def get_params_for_process_completion(processId: int, db: Session = Depends(get_db)):
    return process_crud.get_params_for_process_completion(db, processId=processId)

@router.post("/complete")
async def complete_process_instance(completeProcessObj: CompleteProcess , db: Session = Depends(get_db)):
    # Input - parameters required for the process type
    # Check if this is the last process - if yes then complete the workflow instance as well
    # If not, then complete and update the process instance, update the workflow instance and start the next process
    return process_crud.complete_process(completeProcessObj=completeProcessObj, db=db)
