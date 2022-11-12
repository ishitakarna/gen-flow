from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
import datetime

class ProcessParamInstanceObject(BaseModel):
    paramVal: str
    processInstanceId: int
    paramId: int

class ProcessParamInstanceList(BaseModel):
    paramList: list[ProcessParamInstanceObject]

def get_params_for_process_completion(db: Session, processId: int):
    query = text('select * from Parameters where processId = {processId}'.format(processId= processId))
    result = db.execute(query)
    process_params = list(result.fetchall())
    return process_params

def complete_process(processInstanceId: int, wfInstanceId: int, processId: int, processParamInstances: ProcessParamInstanceList, db: Session):
    query_last_process = text('select max(processId) as pr from Processes where wfId = (select wfId from (select wfInstanceId from ProcessInstances where processInstanceId = {processInstanceId}) as ABC join WorkflowInstances on WorkflowInstances.wfInstanceId = ABC.wfInstanceId)'.format(processInstanceId=processInstanceId))
    result_last_process = db.execute(query_last_process)

    # Update completed time of process instance
    completedDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updatedDT = completedDT
    createdDT = completedDT

    query_update_process_instance = text('update ProcessInstances set completedDT = \'{completedDT}\' where processInstanceId = {processInstanceId}'.format(completedDT=completedDT, updatedDT=updatedDT, processInstanceId=processInstanceId))
    db.execute(query_update_process_instance)
    
    if result_last_process.fetchone()['pr'] == processId:
        # complete time of workflow instance
        query_update_wf_instance = text('update WorkflowInstances set completedDT = \'{completedDT}\', updatedDT = \'{updatedDT}\' where wfInstanceId = {wfInstanceId}'.format(completedDT=completedDT, updatedDT=updatedDT, wfInstanceId=wfInstanceId))
        db.execute(query_update_wf_instance)
    else:
        query_update_wf_instance = text('update WorkflowInstances set updatedDT = \'{updatedDT}\' where wfInstanceId = {wfInstanceId}'.format(updatedDT=updatedDT, wfInstanceId=wfInstanceId))
        db.execute(query_update_wf_instance)
        # Create next process instance
        query_insert_process_instance = text('insert into ProcessInstances (createdDT, completedDT, processId, wfInstanceId) values (\'{createdDT}\',\'{completedDT}\', {processId}, {wfInstanceId})'.format(createdDT=createdDT, completedDT=completedDT, processId=processId + 1, wfInstanceId=wfInstanceId))
        db.execute(query_insert_process_instance)

    return {"Updated Process": True}

