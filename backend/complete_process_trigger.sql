DROP TRIGGER complete_process_trigger;
DELIMITER //
CREATE TRIGGER complete_process_trigger
    AFTER INSERT
    ON CompletedProcesses FOR EACH ROW
    BEGIN
        UPDATE ProcessInstances set completedDT = now() where processInstanceId = new.processInstanceId;
        SET @next_process_id = (select processId from Processes where wfId= new.wfId and seqNumber= new.seqNumber+1);
        IF @next_process_id is null THEN
            UPDATE WorkflowInstances SET completedDT = now(), updatedDT = now() WHERE wfInstanceId = new.wfInstanceId;
        ELSE
            UPDATE WorkflowInstances set updatedDT = now() where wfInstanceId = new.wfInstanceId;
            INSERT INTO ProcessInstances (createdDT, completedDT, processId, wfInstanceId) values (now(), '2001-01-01 00:00:00', @next_process_id, new.wfInstanceId);
        END IF;
    END;
//
DELIMITER ;

update ProcessInstances set completedDT=NOW() where processInstanceId=48;

create table CompletedProcesses(
        wfId integer,
        wfInstanceId integer,
        processInstanceId integer,
        seqNumber integer)
