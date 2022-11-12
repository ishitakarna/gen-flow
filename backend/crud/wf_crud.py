from sqlalchemy.orm import Session
from sqlalchemy import text
import datetime

def get_workflow_types_for_business(db: Session, businessId: int):
    query = text('select * from Workflows where businessId = {businessId}'.format(businessId= businessId))
    result = db.execute(query)
    workflow_obj_arr = list(result.fetchall())
    return workflow_obj_arr

def get_incomplete_workflow_instances_for_business(db: Session, businessId: int):
    wf_ins_join_wf = 'select wfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, completedDT as wfcompletedDT, Workflows.wfId, wfName, wfDescription, businessId from WorkflowInstances join Workflows on Workflows.wfId = WorkflowInstances.wfId where completedDT <= \"2001-01-01T00:00:00\" and businessId = {businessId} order by createdDT desc limit 10'.format(businessId = businessId)
    query = text('select * from Processes join ProcessInstances on Processes.processId = ProcessInstances.processId join ({wf_ins_join_wf}) as ABC on ABC.wfId = Processes.wfId and ABC.wfInstanceId = ProcessInstances.wfInstanceId join Parameters on Parameters.processId = Processes.processId join ParamInstances on Parameters.paramId = ParamInstances.paramId and ParamInstances.processInstanceId = ProcessInstances.processInstanceId'.format(wf_ins_join_wf=wf_ins_join_wf))
    print(query)
    result = db.execute(query)
    workflow_obj_arr = list(result.fetchall())
    return workflow_obj_arr

def add_workflow_instance(db: Session, wfId: int):
    createdDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # wfInstanceId = int(db.execute(text('select max(wfInstanceId) from WorkflowInstances')).first()[0])+1
    # print(wfInstanceId[0])
    print(datetime.datetime(1, 1, 1, 0, 0))

    query = text('insert into WorkflowInstances (createdDT,wfId, updatedDT, completedDT) values (\''+createdDT+'\','+str(wfId)+',\''+datetime.datetime.strptime('0000-00-00 00:00:00', "%Y-%m-%d %H:%M:%S")+',\''+datetime.datetime.strptime('0000-00-00 00:00:00', "%Y-%m-%d %H:%M:%S")+'\'')
    print(query)
    # result = db.execute(query)
    # return result.fetchall()
    return {"hehe": True}