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
    view_j1_wf_ins_join_wf = 'create or replace view j1WfInsJoinWf as select wfInstanceId as j1WfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, completedDT as wfcompletedDT, Workflows.wfId as j1WfId, wfName, wfDescription, businessId as j1BusinessId from WorkflowInstances join Workflows on Workflows.wfId = WorkflowInstances.wfId where completedDT = \"2001-01-01T00:00:00\" and businessId = {businessId}'.format(
        businessId=businessId)
    view_j2_pro_ins_join_pro = 'create or replace view j2ProInsJoinPro as select Processes.processId as j2ProcessId, processName, seqNumber, wfId as j2WfId, processInstanceId as j2ProcessInstanceId, createdDT as processInstanceCreatedDT, completedDT as processInstanceCompletedDT, wfInstanceId as j2WfInstanceId from Processes join ProcessInstances on Processes.processId = ProcessInstances.processId'
    view_j3_j1_join_j2 = 'create or replace view j3J1JoinJ2 as select * from j1WfInsJoinWf join j2ProInsJoinPro on j1WfInsJoinWf.j1WfId = j2ProInsJoinPro.j2WfId and j1WfInsJoinWf.j1WfInstanceId = j2ProInsJoinPro.j2WfInstanceId'
    view_j4_j3_join_params = 'create or replace view j4J3JoinParam as select * from j3J1JoinJ2 join Parameters on j3J1JoinJ2.j2ProcessId = Parameters.processId'
    view_j5_j4_join_param_ins = 'create or replace view j5J4JoinParamIns as select j1WfInstanceId as wfInstanceId, wfcreatedDT, wfupdatedDT, wfcompletedDT, j1WfId as wfId, wfName, wfDescription, j1BusinessId as businessId, j2ProcessId as processId, processName, seqNumber, j2ProcessInstanceId as processInstanceId, processInstanceCreatedDT, processInstanceCompletedDT, j4J3JoinParam.paramId as paramId, paramName, paramType, isOptional, paramVal from j4J3JoinParam left join ParamInstances on j4J3JoinParam.paramId = ParamInstances.paramId and j4J3JoinParam.j2ProcessInstanceId = ParamInstances.processInstanceId'

    result = db.execute(view_j1_wf_ins_join_wf)
    result = db.execute(view_j2_pro_ins_join_pro)
    result = db.execute(view_j3_j1_join_j2)
    result = db.execute(view_j4_j3_join_params)
    result = db.execute(view_j5_j4_join_param_ins)
    result = db.execute('select * from j5J4JoinParamIns')

    workflow_obj_arr = list(result.fetchall())
    hashmap = []
    for key, group in itertools.groupby(workflow_obj_arr, lambda item: item["wfInstanceId"]):
        group,tp = itertools.tee(group)
        tp = list(tp)
        temp = {}
        temp["wfInstancceId"] = key
        temp["wfId"] = tp[0]["wfId"]
        temp["businessId"] = tp[0]["businessId"]
        temp["wfcreatedDT"] = tp[0]["wfcreatedDT"]
        temp["wfupdatedDT"] = tp[0]["wfupdatedDT"]
        temp["wfcompletedDT"] = tp[0]["wfcompletedDT"]
        temp["wfName"] = tp[0]["wfName"]
        temp["wfDescription"] = tp[0]["wfDescription"]
        hashmap1 = []
        for key1,group1 in itertools.groupby(group, lambda item1: item1["processInstanceId"]):
            group1, tp1 = itertools.tee(group1)
            tp1 = list(tp1)
            temp2 = {}
            temp2["processInstanceId"] = key1
            temp2["paramInstances"] = []
            temp2["processInstanceCreatedDT"] = tp1[0]["processInstanceCreatedDT"]
            temp2["processInstanceCompletedDT"] = tp1[0]["processInstanceCompletedDT"]
            temp2["seqNumber"] = tp1[0]["seqNumber"]
            temp2["processName"] = tp1[0]["processName"]
            temp2["processId"] = tp1[0]["processId"]
            for item1 in group1:
                tp3 = {}
                tp3["paramId"] = item1["paramId"]
                tp3["paramName"] = item1["paramName"]
                tp3["paramType"] = item1["paramType"]
                tp3["isOptional"] = item1["isOptional"]
                tp3["paramVal"] = item1["paramVal"]
                temp2["paramInstances"].append(tp3)
            hashmap1.append(temp2)
        temp["processInstances"] = hashmap1
        hashmap.append(temp)
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