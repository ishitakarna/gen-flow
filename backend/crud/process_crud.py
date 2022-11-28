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
        query_insert_completed_processes = text(
            'insert into CompletedProcesses (wfId, wfInstanceId, processInstanceId,seqNumber )'
            ' values ({wfId}, {wfInstanceId}, {processInstanceId}, {seqNumber})'
            .format(wfId=wfId, wfInstanceId=wfInstanceId, processInstanceId=processInstanceId, seqNumber=seqNumber))
        db.execute(query_insert_completed_processes)
        db.commit()
    except:
        db.rollback()
        raise
    return {"Updated Process": True}