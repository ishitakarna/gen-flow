from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List
import datetime

class ProcessParamInstanceObject(BaseModel):
    paramVal: str
    processInstanceId: int
    paramId: int

class ProcessParamInstanceList(BaseModel):
    paramList: List[ProcessParamInstanceObject]

def get_params_for_process_completion(db: Session, processId: int):
    query = text('select * from Parameters where processId = {processId}'.format(processId= processId))
    result = db.execute(query)
    process_params = list(result.fetchall())
    return process_params

def complete_process(wfId: int,wfInstanceId: int, processInstanceId: int, seqNumber: int, processParamInstances: ProcessParamInstanceList, db: Session):
    db.begin()
    try:
        completedDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updatedDT = completedDT
        createdDT = completedDT

        query_update_process_instance = text('update ProcessInstances set completedDT = \'{completedDT}\' where processInstanceId = {processInstanceId}'.format(completedDT=completedDT, updatedDT=updatedDT, processInstanceId=processInstanceId))
        db.execute(query_update_process_instance)

        query_next_process_id = text(
            'select processId from Processes where wfId= {wfId} and seqNumber= {seqNumber}'.format(wfId=wfId,
                                                                                                  seqNumber=seqNumber + 1))
        result_next_process_id = db.execute(query_next_process_id)
        result_next_process_id = result_next_process_id.fetchone()
        print(result_next_process_id)
        if result_next_process_id:
            query_update_wf_instance = text(
                'update WorkflowInstances set updatedDT = \'{updatedDT}\' where wfInstanceId = {wfInstanceId}'.format(
                    updatedDT=updatedDT, wfInstanceId=wfInstanceId))
            db.execute(query_update_wf_instance)

            query_insert_process_instance = text(
                'insert into ProcessInstances (createdDT, completedDT, processId, wfInstanceId) values (\'{createdDT}\',\'{completedDT}\', {processId}, {wfInstanceId})'.format(
                    createdDT=createdDT,
                    completedDT=str(datetime.datetime.strptime('2001-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")),
                    processId=result_next_process_id[0], wfInstanceId=wfInstanceId))
            db.execute(query_insert_process_instance)
        else:
            query_update_wf_instance = text(
                'update WorkflowInstances set completedDT = \'{completedDT}\', updatedDT = \'{updatedDT}\' where wfInstanceId = {wfInstanceId}'.format(
                    completedDT=completedDT, updatedDT=updatedDT, wfInstanceId=wfInstanceId))
            db.execute(query_update_wf_instance)
        db.commit()
    except:
        db.rollback()
        raise
    return {"Updated Process": True}