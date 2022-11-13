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
    wf_ins_join_wf = 'select wfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, completedDT as wfcompletedDT, Workflows.wfId, wfName, wfDescription, businessId from WorkflowInstances join Workflows on Workflows.wfId = WorkflowInstances.wfId where completedDT = \"2001-01-01T00:00:00\" and businessId = {businessId}'.format(businessId = businessId)
    query = text(
        'select * from Processes join ProcessInstances on Processes.processId = ProcessInstances.processId join ({wf_ins_join_wf}) as ABC on ABC.wfId = Processes.wfId and ABC.wfInstanceId = ProcessInstances.wfInstanceId left join (select processId as paramProcessId, paramName, paramId from Parameters) as params on params.paramProcessId = Processes.processId left join (select paramVal, processInstanceId as prProcessInstanceId, paramId as prParamId from ParamInstances) as ParamInstancesSQ on params.paramId = ParamInstancesSQ.prParamId and ParamInstancesSQ.prProcessInstanceId = ProcessInstances.processInstanceId order by ABC.wfupdatedDT desc'.format(
            wf_ins_join_wf=wf_ins_join_wf))
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

def delete_workflow_instance(db: Session, wfInstanceId: int, businessId: int):
    query = text('delete from WorkflowInstances where wfInstanceId = {wfInstanceId}'.format(wfInstanceId=wfInstanceId))
    result = db.execute(query)
    return get_incomplete_workflow_instances_for_business(db,businessId=businessId)

def get_incomplete_workflow_instances_for_user(db: Session, userId: int):
    query = text('select * from (select * from ProcessInstances where wfInstanceId in (select wfInstanceId from ProcessInstances join (select processId from Processes where deptId=(select deptId from UserDepartment where userId={userId})) as pro on ProcessInstances.processId=pro.processId where completedDT="2001-01-01T00:00:00")) as proI left join (select * from ParamInstances natural join Parameters) as par on proI.processInstanceId=par.processInstanceId;'.format(userId=userId))
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

def report_completed_counts(db: Session, businessId: int):
    query = text('select count(wi.wfInstanceId) as completedWFInstances, wfName from (select * from Workflows where businessId='+str(businessId)+') as  w join WorkflowInstances wi using (wfId) where wi.completedDT != \"2001-01-01T00:00:00\" group by wfId')
    result = db.execute(query)
    return list(result.fetchall())