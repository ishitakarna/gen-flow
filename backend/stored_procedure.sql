delimiter //
create procedure AddWorkflowInstance (IN workflowId INT)
begin
    declare varWfInstanceId INT;
    declare varProcessId INT;
    DECLARE businessWorkflowCount INT DEFAULT 0;
    DECLARE exit_loop BOOLEAN DEFAULT FALSE;

    -- Cursor
    DECLARE wf_ins_cur CURSOR FOR (select distinct wfInstanceId from WorkflowInstances);
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;

    insert into WorkflowInstances(createdDT, wfId, updatedDT, completedDT) values (NOW(), workflowId, '2001-01-01T00:00:00', '2001-01-01T00:00:00'); 
    select max(wfInstanceId) into @varWfInstanceId from WorkflowInstances;
    select processId into @varProcessId from Processes where seqNumber=1 and wfId=workflowId;
    insert into ProcessInstances(createdDT, completedDT, processId, wfInstanceId) values
        (NOW(), '2001-01-01T00:00:00', @varProcessId, @varWfInstanceId);

    create or replace view j1WfInsJoinWf as select wfInstanceId 
        as j1WfInstanceId, createdDT as wfcreatedDT, updatedDT as wfupdatedDT, 
        completedDT as wfcompletedDT, Workflows.wfId as j1WfId, wfName, 
        wfDescription, businessId as j1BusinessId from WorkflowInstances 
        join Workflows on Workflows.wfId = WorkflowInstances.wfId 
        where completedDT = "2001-01-01T00:00:00" and businessId = 1;

    create or replace view j2ProInsJoinPro as select 
        Processes.processId as j2ProcessId, processName, seqNumber, 
        wfId as j2WfId, processInstanceId as j2ProcessInstanceId, 
        createdDT as processInstanceCreatedDT, 
        completedDT as processInstanceCompletedDT, 
        wfInstanceId as j2WfInstanceId, deptId from Processes join 
        ProcessInstances on Processes.processId = ProcessInstances.processId;

    create or replace view j3J1JoinJ2 as select * from j1WfInsJoinWf 
        join j2ProInsJoinPro on j1WfInsJoinWf.j1WfId = j2ProInsJoinPro.j2WfId 
        and j1WfInsJoinWf.j1WfInstanceId = j2ProInsJoinPro.j2WfInstanceId;

    create or replace view j4J3JoinParam as select * from j3J1JoinJ2 
        left join Parameters on j3J1JoinJ2.j2ProcessId = Parameters.processId;

    create or replace view j5J4JoinParamIns as select j1WfInstanceId as 
        wfInstanceId, wfcreatedDT, wfupdatedDT, wfcompletedDT, j1WfId as wfId, 
        wfName, wfDescription, j1BusinessId as businessId, j2ProcessId as processId, 
        processName, seqNumber, j2ProcessInstanceId as processInstanceId, 
        processInstanceCreatedDT, processInstanceCompletedDT, 
        j4J3JoinParam.paramId as paramId, paramName, paramType, 
        isOptional, paramVal, deptId from j4J3JoinParam left join 
        ParamInstances on j4J3JoinParam.paramId = ParamInstances.paramId 
        and j4J3JoinParam.j2ProcessInstanceId = ParamInstances.processInstanceId 
        order by wfcreatedDT desc;

    CREATE TABLE IF NOT EXISTS BusinessWorkflowsCount (
        pendingWorkflowsCount INTEGER,
        recordedDate DATE
    );

    OPEN wf_ins_cur;
    cloop: LOOP 
        FETCH wf_ins_cur INTO varWfInstanceId;
        SET businessWorkflowCount = businessWorkflowCount + 1;

        -- Loop break condition
        IF(exit_loop) THEN
            LEAVE cloop;
        END IF;

    END LOOP cloop;
    CLOSE wf_ins_cur;

    insert into BusinessWorkflowsCount (pendingWorkflowsCount, recordedDate) 
        values (businessWorkflowCount, NOW());

end //
delimiter ;

-- Other utilities
-- drop procedure AddWorkflowInstance;

-- Calling procedure
-- call AddWorkflowInstance(1);

-- Testing
-- select * from WorkflowInstances order by wfInstanceId desc limit 10;
-- select * from ProcessInstances order by processInstanceId desc limit 10;
-- select * from BusinessWorkflowsCount;


-- Recovery
-- delete from WorkflowInstances where wfInstanceId > 1000;
    
