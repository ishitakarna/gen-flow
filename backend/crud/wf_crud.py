import os

from sqlalchemy.orm import Session
from sqlalchemy import text
import datetime
import itertools
import matplotlib.pyplot as plt
import base64
from matplotlib import pyplot as pyplt

def jsonify_workflow_result(workflow_obj_arr):
    hashmap = []
    for key, group in itertools.groupby(workflow_obj_arr, lambda item: item["wfInstanceId"]):
        group,tp = itertools.tee(group)
        tp = list(tp)
        temp = {}
        temp["wfInstanceId"] = key
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
            tp1.sort(key = lambda x: x["seqNumber"])
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
                if item1["paramId"]:
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

def get_workflow_types_for_business(db: Session, businessId: int):
    query = text('select * from Workflows where businessId = {businessId}'.format(businessId= businessId))
    result = db.execute(query)
    workflow_obj_arr = list(result.fetchall())
    return workflow_obj_arr

def get_incomplete_workflow_instances_for_business(db: Session, businessId: int):
    view_j1_wf_ins_join_wf = 'create or replace view j1WfInsJoinWf as select wfInstanceId as j1WfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, completedDT as wfcompletedDT, Workflows.wfId as j1WfId, wfName, wfDescription, businessId as j1BusinessId from WorkflowInstances join Workflows on Workflows.wfId = WorkflowInstances.wfId where completedDT = \"2001-01-01T00:00:00\" and businessId = {businessId}'.format(businessId=businessId)
    view_j2_pro_ins_join_pro = 'create or replace view j2ProInsJoinPro as select Processes.processId as j2ProcessId, processName, seqNumber, wfId as j2WfId, processInstanceId as j2ProcessInstanceId, createdDT as processInstanceCreatedDT, completedDT as processInstanceCompletedDT, wfInstanceId as j2WfInstanceId from Processes join ProcessInstances on Processes.processId = ProcessInstances.processId'
    view_j3_j1_join_j2 = 'create or replace view j3J1JoinJ2 as select * from j1WfInsJoinWf join j2ProInsJoinPro on j1WfInsJoinWf.j1WfId = j2ProInsJoinPro.j2WfId and j1WfInsJoinWf.j1WfInstanceId = j2ProInsJoinPro.j2WfInstanceId'
    view_j4_j3_join_params = 'create or replace view j4J3JoinParam as select * from j3J1JoinJ2 left join Parameters on j3J1JoinJ2.j2ProcessId = Parameters.processId'
    view_j5_j4_join_param_ins = 'create or replace view j5J4JoinParamIns as select j1WfInstanceId as wfInstanceId, wfcreatedDT, wfupdatedDT, wfcompletedDT, j1WfId as wfId, wfName, wfDescription, j1BusinessId as businessId, j2ProcessId as processId, processName, seqNumber, j2ProcessInstanceId as processInstanceId, processInstanceCreatedDT, processInstanceCompletedDT, j4J3JoinParam.paramId as paramId, paramName, paramType, isOptional, paramVal from j4J3JoinParam left join ParamInstances on j4J3JoinParam.paramId = ParamInstances.paramId and j4J3JoinParam.j2ProcessInstanceId = ParamInstances.processInstanceId order by wfcreatedDT desc'

    result = db.execute(view_j1_wf_ins_join_wf)
    result = db.execute(view_j2_pro_ins_join_pro)
    result = db.execute(view_j3_j1_join_j2)
    result = db.execute(view_j4_j3_join_params)
    result = db.execute(view_j5_j4_join_param_ins)
    result = db.execute('select * from j5J4JoinParamIns')

    workflow_obj_arr = list(result.fetchall())
    return jsonify_workflow_result(workflow_obj_arr)

# Stored Procedure Call
def add_workflow_instance(db: Session, wfId: int, businessId: int):
    call_proc = 'call AddWorkflowInstance({wfId})'.format(wfId = wfId)
    db.execute(call_proc)
    result = db.execute('select * from j5J4JoinParamIns')
    return jsonify_workflow_result(result)

def search_workflowInstance_by_wfInstanceId(db: Session, wfInstanceId: int):
    q1 = 'create or replace view j1WfInsJoinWf as select wfInstanceId as j1WfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, completedDT as wfcompletedDT, Workflows.wfId as j1WfId, wfName, wfDescription, businessId as j1BusinessId from WorkflowInstances join Workflows on Workflows.wfId = WorkflowInstances.wfId where wfInstanceId = {wfInstanceId}'.format(wfInstanceId=wfInstanceId)
    q2 = 'create or replace view j2ProInsJoinPro as select Processes.processId as j2ProcessId, processName, seqNumber, wfId as j2WfId, processInstanceId as j2ProcessInstanceId, createdDT as processInstanceCreatedDT, completedDT as processInstanceCompletedDT, wfInstanceId as j2WfInstanceId from Processes join ProcessInstances on Processes.processId = ProcessInstances.processId'
    q3 = 'create or replace view j3J1JoinJ2 as select * from j1WfInsJoinWf join j2ProInsJoinPro on j1WfInsJoinWf.j1WfId = j2ProInsJoinPro.j2WfId and j1WfInsJoinWf.j1WfInstanceId = j2ProInsJoinPro.j2WfInstanceId'
    q4 = 'create or replace view j4J3JoinParam as select * from j3J1JoinJ2 left join Parameters on j3J1JoinJ2.j2ProcessId = Parameters.processId'
    q5 = 'create or replace view j5J4JoinParamIns as select j1WfInstanceId as wfInstanceId, wfcreatedDT, wfupdatedDT, wfcompletedDT, j1WfId as wfId, wfName, wfDescription, j1BusinessId as businessId, j2ProcessId as processId, processName, seqNumber, j2ProcessInstanceId as processInstanceId, processInstanceCreatedDT, processInstanceCompletedDT, j4J3JoinParam.paramId as paramId, paramName, paramType, isOptional, paramVal from j4J3JoinParam left join ParamInstances on j4J3JoinParam.paramId = ParamInstances.paramId and j4J3JoinParam.j2ProcessInstanceId = ParamInstances.processInstanceId'
    result = db.execute(q1)
    result = db.execute(q2)
    result = db.execute(q3)
    result = db.execute(q4)
    result = db.execute(q5)
    result = db.execute('select * from j5J4JoinParamIns')
    workflow_obj_arr = list(result.fetchall())
    return jsonify_workflow_result(workflow_obj_arr)

def delete_workflow_instance(db: Session, wfInstanceId: int, businessId: int):
    query = text('delete from WorkflowInstances where wfInstanceId = {wfInstanceId}'.format(wfInstanceId=wfInstanceId))
    db.execute(query)
    return get_incomplete_workflow_instances_for_business(db,businessId=businessId)

def get_incomplete_workflow_instances_for_user(db: Session, userId: int):
    view_j1_wf_ins_join_wf = 'create or replace view j1WfInsJoinWf as select wfInstanceId as j1WfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, completedDT as wfcompletedDT, Workflows.wfId as j1WfId, wfName, wfDescription, businessId as j1BusinessId from WorkflowInstances join Workflows on Workflows.wfId = WorkflowInstances.wfId where completedDT = \"2001-01-01T00:00:00\"'
    view_j2_pro_ins_join_pro = 'create or replace view j2ProInsJoinPro as select Processes.processId as j2ProcessId, processName, seqNumber, wfId as j2WfId, processInstanceId as j2ProcessInstanceId, createdDT as processInstanceCreatedDT, completedDT as processInstanceCompletedDT, wfInstanceId as j2WfInstanceId from Processes join ProcessInstances on Processes.processId = ProcessInstances.processId'
    view_j3_j1_join_j2 = 'create or replace view j3J1JoinJ2 as select * from j1WfInsJoinWf join j2ProInsJoinPro on j1WfInsJoinWf.j1WfId = j2ProInsJoinPro.j2WfId and j1WfInsJoinWf.j1WfInstanceId = j2ProInsJoinPro.j2WfInstanceId'
    view_j4_j3_join_params = 'create or replace view j4J3JoinParam as select * from j3J1JoinJ2 left join Parameters on j3J1JoinJ2.j2ProcessId = Parameters.processId'
    view_j5_j4_join_param_ins = 'create or replace view j5J4JoinParamIns as select j1WfInstanceId as wfInstanceId, wfcreatedDT, wfupdatedDT, wfcompletedDT, j1WfId as wfId, wfName, wfDescription, j1BusinessId as businessId, j2ProcessId as processId, processName, seqNumber, j2ProcessInstanceId as processInstanceId, processInstanceCreatedDT, processInstanceCompletedDT, j4J3JoinParam.paramId as paramId, paramName, paramType, isOptional, paramVal from j4J3JoinParam left join ParamInstances on j4J3JoinParam.paramId = ParamInstances.paramId and j4J3JoinParam.j2ProcessInstanceId = ParamInstances.processInstanceId order by wfcreatedDT desc'
    view_user_wf_instances = 'create or replace view userWfInstances as select wfInstanceId from ProcessInstances where processId in (select processId from Processes where deptId in (select deptId from UserDepartment where userId={userId}) and completedDT = "2001-01-01T00:00:00")'.format(userId = userId)

    result = db.execute(view_j1_wf_ins_join_wf)
    result = db.execute(view_j2_pro_ins_join_pro)
    result = db.execute(view_j3_j1_join_j2)
    result = db.execute(view_j4_j3_join_params)
    result = db.execute(view_j5_j4_join_param_ins)
    result = db.execute(view_user_wf_instances)
    result = db.execute('select * from j5J4JoinParamIns where wfInstanceId in (select * from userWfInstances)')

    workflow_obj_arr = list(result.fetchall())
    return jsonify_workflow_result(workflow_obj_arr)

def report_completed_counts(db: Session, businessId: int):
    query = text('select count(wi.wfInstanceId) as completedWFInstances, wfName from (select * from Workflows where businessId='+str(businessId)+') as  w join WorkflowInstances wi using (wfId) where wi.completedDT != \"2001-01-01T00:00:00\" group by wfId')
    result = db.execute(query)
    query1 = text('select year(completedDT) as year, count(*) as count from WorkflowInstances where wfId in (select wfId from Workflows where businessId={businessId}) group by year(completedDT) order by year(completedDT);'.format(businessId=businessId))
    result1 = db.execute(query1)
    result1 = result1.fetchall()
    years = [i[0] for i in result1]
    counts = [i[1] for i in result1]
    plt.plot(years, counts)
    plt.xlabel('Years')
    plt.ylabel('# Completed Workflows')
    plt.title("Workflow Completion Trend")
    if os.path.exists("trends.png"):
        os.remove("trends.png")
    plt.savefig("trends.png")
    with open("trends.png", "rb") as img_file:
        trends = base64.b64encode(img_file.read())
    # plt.show()
    plt.close()
    query2 = text('select floor(avg(datediff(createdDT, completedDT))) as avg_turn_around_days, deptName as department from Workflows JOIN Processes on Workflows.wfId=Processes.wfId JOIN Departments ON Processes.deptId=Departments.deptId JOIN ProcessInstances ON Processes.processId=ProcessInstances.processId where Workflows.businessId={businessId} group by Processes.deptId'.format(businessId=businessId))
    result2 = db.execute(query2)
    result2 = result2.fetchall()
    departments= [i[0] for i in result2]
    avg_turn_around_days = [i[1] for i in result2]
    pyplt.bar(avg_turn_around_days, departments)
    pyplt.xlabel('Department')
    pyplt.ylabel('Avg. Turn Around Days')
    pyplt.title("Department velocities")
    if os.path.exists("velocities.png"):
        os.remove("velocities.png")
    pyplt.savefig("velocities.png")
    # pyplt.show()
    with open("velocities.png", "rb") as img_file:
        velocities = base64.b64encode(img_file.read())
    return {"completed_counts": list(result.fetchall()), "trend_image": trends, "velocities_image": velocities}