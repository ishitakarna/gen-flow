delimiter //
create procedure AddWorkflowInstance (IN wfId INT)
begin
    declare varWfInstanceId INT;
    declare varProcessId INT;
    insert into WorkflowInstances(createdDT, wfId, updatedDT, completedDT) values (NOW(), wfId, '2001-01-01T00:00:00', '2001-01-01T00:00:00'); 
    select max(wfInstanceId) into @varWfInstanceId from WorkflowInstances;
    select processId into @varProcessId from Processes where seqNumber = 1 and wfId = @wfId;
    insert into ProcessInstances(createdDT, completedDT, processId, wfInstanceId) values
        (NOW(), '2001-01-01T00:00:00', @varProcessId, @varWfInstanceId);
end //
delimiter ;

-- Other utilities
-- drop procedure AddWorkflowInstance;

-- Calling procedure
-- call AddWorkflowInstance(1);

-- Testing
-- select * from WorkflowInstances order by wfInstanceId desc limit 10;
-- select * from ProcessInstances order by processInstanceId desc limit 10;