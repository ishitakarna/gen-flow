from sqlalchemy.orm import Session
from sqlalchemy import text

def get_params_for_process_completion(db: Session, processId: int):
    query = text('select * from Parameters where processId = {processId}'.format(processId= processId))
    result = db.execute(query)
    process_params = list(result.fetchall())
    return process_params

# TODO: Test
# def delete_workflow_instance(db: Session, wfInstanceId: int, businessId: int):
#     query = text('delete from WorkflowInstances where wfInstanceId = {wfInstanceId}'.format(wfInstanceId=wfInstanceId))
#     result = db.execute(query)
#     return get_incomplete_workflow_instances_for_business(db,businessId=businessId)