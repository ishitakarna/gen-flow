from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel



def get_params_for_process_completion(db: Session, processId: int):
    query = text('select * from Parameters where processId = {processId}'.format(processId= processId))
    result = db.execute(query)
    process_params = list(result.fetchall())
    return process_params

def complete_process(processInstanceId: int, processParamInstances, db: Session):

    # Get workflow id from process instance id and 
    # select wfId from (select wfInstanceId from ProcessInstances where processInstanceId = {processInstanceId}) as ABC join WorkflowInstances on WorkflowInstances.wfInstanceId = ABC.wfInstanceId
    # Get max process id
    # select max(processId) from Processes where wfId = (select wfId from (select wfInstanceId from ProcessInstances where processInstanceId = {processInstanceId}) as ABC join WorkflowInstances on WorkflowInstances.wfInstanceId = ABC.wfInstanceId)


    pass
