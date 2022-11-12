from sqlalchemy.orm import Session
from sqlalchemy import text
import datetime
import itertools

def get_workflow_types_for_business(db: Session, businessId: int):
    query = text('select * from Workflows where businessId = {businessId}'.format(businessId= businessId))
    result = db.execute(query)
    workflow_obj_arr = list(result.fetchall())
    return workflow_obj_arr

def get_incomplete_workflow_instances_for_business(db: Session, businessId: int):
    wf_ins_join_wf = 'select wfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, completedDT as wfcompletedDT, Workflows.wfId, wfName, wfDescription, businessId from WorkflowInstances join Workflows on Workflows.wfId = WorkflowInstances.wfId where completedDT = \"2001-01-01T00:00:00\" and businessId = {businessId} order by createdDT desc'.format(businessId = businessId)
    query = text('select * from Processes join ProcessInstances on Processes.processId = ProcessInstances.processId join ({wf_ins_join_wf}) as ABC on ABC.wfId = Processes.wfId and ABC.wfInstanceId = ProcessInstances.wfInstanceId left join Parameters on Parameters.processId = Processes.processId left join (select paramVal, processInstanceId as prProcessInstanceId, paramId as prParamId from ParamInstances) as ParamInstancesSQ on Parameters.paramId = ParamInstancesSQ.prParamId and ParamInstancesSQ.prProcessInstanceId = ProcessInstances.processInstanceId'.format(wf_ins_join_wf=wf_ins_join_wf))
    print(query)
    result = db.execute(query)
    workflow_obj_arr = list(result.fetchall())
    hashmap = {}
    for key, group in itertools.groupby(workflow_obj_arr, lambda item: item["wfInstanceId"]):
        hashmap[key] = []
        # hashmap[key] = [item for item in group]
        hashmap1 = {}
        for key1,group1 in itertools.groupby(group, lambda item1: item1["processInstanceId"]):
            # print(key1, group1)
            hashmap1[key1] = [item1 for item1 in group1]
        hashmap[key].append(hashmap1)
    return hashmap

def add_workflow_instance(db: Session, wfId: int, businessId: int):
    createdDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = text('insert into WorkflowInstances (createdDT,wfId, updatedDT, completedDT) values (\''+createdDT+'\','+str(wfId)+',\''+str(datetime.datetime.strptime('2001-01-01 00:00:00', "%Y-%m-%d %H:%M:%S"))+'\',\''+str(datetime.datetime.strptime('2001-01-01 00:00:00', "%Y-%m-%d %H:%M:%S"))+'\')')
    result = db.execute(query)
    query1 = text('select max(wfInstanceId) from WorkflowInstances')
    wfInstanceId = db.execute(query1).first()[0]
    query2 = text('select processId from Processes where seqNumber=1 and wfId='+str(wfId))
    processId = db.execute(query2).first()[0]
    query3 = text('insert into ProcessInstances(createdDT, completedDT, processId, wfInstanceId) values (\''+createdDT+'\',\''+str(datetime.datetime.strptime('2001-01-01 00:00:00', "%Y-%m-%d %H:%M:%S"))+'\','+str(processId)+','+str(wfInstanceId)+')')
    db.execute(query3)
    return get_incomplete_workflow_instances_for_business(db,businessId=businessId)

def search_workflowInstance_by_wfInstanceId(db: Session, wfInstanceId: int):
    wf_ins_join_wf = 'select wfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, completedDT as wfcompletedDT, Workflows.wfId, wfName, wfDescription, businessId from WorkflowInstances join Workflows on Workflows.wfId = WorkflowInstances.wfId where wfInstanceId={wfInstanceId} order by createdDT desc'.format(wfInstanceId=wfInstanceId)
    query = text(
        'select * from Processes join ProcessInstances on Processes.processId = ProcessInstances.processId join ({wf_ins_join_wf}) as ABC on ABC.wfId = Processes.wfId and ABC.wfInstanceId = ProcessInstances.wfInstanceId left join Parameters on Parameters.processId = Processes.processId left join (select paramVal, processInstanceId as prProcessInstanceId, paramId as prParamId from ParamInstances) as ParamInstancesSQ on Parameters.paramId = ParamInstancesSQ.prParamId and ParamInstancesSQ.prProcessInstanceId = ProcessInstances.processInstanceId'.format(
            wf_ins_join_wf=wf_ins_join_wf))
    print(query)
    result = db.execute(query)
    workflow_obj_arr = list(result.fetchall())
    hashmap = {}
    for key, group in itertools.groupby(workflow_obj_arr, lambda item: item["wfInstanceId"]):
        hashmap[key] = []
        # hashmap[key] = [item for item in group]
        hashmap1 = {}
        for key1, group1 in itertools.groupby(group, lambda item1: item1["processInstanceId"]):
            # print(key1, group1)
            hashmap1[key1] = [item1 for item1 in group1]
        hashmap[key].append(hashmap1)
    return hashmap