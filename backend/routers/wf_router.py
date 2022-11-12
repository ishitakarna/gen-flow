from fastapi import APIRouter, Form
from database.mysql import get_db
from crud import wf_crud
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(
    prefix="/workflows",
    tags=["workflows"]
)

@router.get("/metadata/{businessId}")
async def get_workflow_types_for_business(businessId: int, db: Session = Depends(get_db)):
    return wf_crud.get_workflow_types_for_business(db, businessId)

@router.get("/instances/incomplete/{businessId}")
async def get_incomplete_workflow_instances_for_business(businessId: int, db: Session = Depends(get_db)):
    return wf_crud.get_incomplete_workflow_instances_for_business(db, businessId=businessId)

@router.post("/instances/add/{wfId}/{businessId}")
async def add_workflow_instance(wfId: int, businessId: int, db: Session = Depends(get_db)):
    return wf_crud.add_workflow_instance(db, wfId=wfId, businessId=businessId)

@router.get("/instances/search/{wfInstanceId}")
async def search_workflowInstance_by_wfInstanceId(wfInstanceId: int, db: Session = Depends(get_db)):
    return wf_crud.search_workflowInstance_by_wfInstanceId(db, wfInstanceId = wfInstanceId)