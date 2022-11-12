from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from json import loads
from collections import defaultdict
import itertools
import datetime

def get_users_test(db: Session):
    query = text('select * from Users')
    result = db.execute(query)
    names = result.fetchall()
    print(names)
    return {"users": names}

def verify_login(db: Session, emailAddress, pwdHash):
    query = text('select * from Users where emailAddress=\''+emailAddress+'\' and pwdHash=\''+pwdHash+'\'')
    result = db.execute(query)
    user = result.fetchall()
    if len(user)==0:
        return {"status": False, "message": "Incorrect Email/Pwd"}
    return {"status": True, "message": "Successful", "user": user[0]}

def get_all_processes_for_a_department(db: Session, emailAddress):
    # query = text('select processId, processName, wfInstanceId from Processes p join (select max(seqNumber) as maxSeq, w.wfId as wfId, wfInstanceId from WorkflowInstances w join ProcessInstances using (wfInstanceId) join Processes using (processId) group by wfInstanceId) as aP on (aP.maxSeq = p.seqNumber and aP.wfId = p.wfId) where deptId = 1;')
    temp = db.execute('select userId,businessId from Users where emailAddress=\''+emailAddress+'\'')
    userId = temp.first()['userId']
    businessId = temp.first()['businessId']

    deptId = '(select deptId from UserDepartment where userId = (select userId from Users where emailAddress=\''+emailAddress+'\'))'
    pri = '(select * from ProcessInstances where CAST(ProcessInstances.completedDT AS CHAR(20)) =\'0000-00-00 00:00:00\')'
    query = text('select * from (select * from Workflows where businessId = ('+businessId+')) as wf join WorkflowInstances on wf.wfId join (select * from Processes where Processes.deptId='+deptId+') as pro on pro.wfId join '+pri+' as pri on pri.processId join Parameters on Parameters.paramId join ParamInstances on ParamInstances.paramId')
    print(query)
    result = db.execute(query)
    processes = list(result.fetchall())
    # for key, group in itertools.groupby(processes, lambda item: item["wfInstanceId"]):
    #     print(key, [item for item in group])
    return processes

def add_workflow_instance(db: Session, wfId):
    createdDT = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    wfInstanceId = int(db.execute(text('select max(wfInstanceId) from WorkflowInstances')).first()[0])+1
    # print(wfInstanceId[0])
    query = text('insert into WorkflowInstances (wfInstanceId,createdDT,wfId) values ('+str(wfInstanceId)+',\''+createdDT+'\','+str(wfId)+')');
    result = db.execute(query)
    return "List of workflows with details"

def delete_workflow_instance(db: Session, wfInstanceId):
    #Delete query
    query = text('delete from WorkflowInstances where wfInstanceId='+wfInstanceId)
    return "deleted"

def complete_process_instance(db: Session, processInstanceId, params):
    return "Completed"
