from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List
import datetime

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

def get_params_for_process_completion(db: Session, processId: int):
    query = text('select * from Parameters where processId = {processId}'.format(processId= processId))
    result = db.execute(query)
    process_params = list(result.fetchall())
    return process_params

def complete_process(completeProcessObj: CompleteProcess, db: Session):
    db.begin()
    try:
        query_insert_completed_processes = text(
            'insert into CompletedProcesses (wfId, wfInstanceId, processInstanceId,seqNumber )'
            ' values ({wfId}, {wfInstanceId}, {processInstanceId}, {seqNumber})'
            .format(wfId=completeProcessObj.wfId, wfInstanceId=completeProcessObj.wfInstanceId, processInstanceId=completeProcessObj.processInstanceId, seqNumber=completeProcessObj.seqNumber))
        db.execute(query_insert_completed_processes)

        # Insert param instances
        for obj in completeProcessObj.params:
            insert_param = text('insert into ParamInstances(paramVal, processInstanceId, paramId) values (\"{param_val}\", {process_instance_id}, {param_id})'.format(param_val=obj.paramVal, process_instance_id=obj.processInstanceId, param_id=obj.paramId))
            db.execute(insert_param)
        db.commit()
    except:
        db.rollback()
        raise

    return {"Updated Process": True}