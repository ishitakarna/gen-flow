import Form from 'react-bootstrap/Form';
import { useState, useEffect } from "react";
import Api from "../../../api";
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function AddModal({setLoading, setWorkflowInstances, onHide}) {
    const [workflows, setWorkflows] = useState([]);
    const [selectedWF, setSelectedWF] = useState({});
    const api = new Api();

    useEffect(() => {
        getAllWorkflows();
    }, []);

    function getAllWorkflowInstances() {
        const api = new Api();
        const wfData = []
        api.getIncompleteWorkFlowsForBO(1)
            .then(result => {
                let workflows = result.data;
                Object.keys(workflows).forEach(function(key){
                    let wf = {}
                    let val = workflows[key]
                    wf.wfInstanceId = val.wfInstanceId
                    wf.name = val.wfName
                    wf.dateC = val.wfcreatedDT
                    wf.dateU = val.wfupdatedDT
                    wf.curP = val.processInstances[(val.processInstances).length - 1].processName
                    wf.dept = "Data not available"
                    wf.businessId = val.businessId
                    wfData.push(wf)
                })
                setWorkflowInstances(wfData);
                setLoading(false);
            })
    }

    function getAllWorkflows() {
        let test = [];

        api.getWorkflowsForB(1)
            .then(result => {
                test = result.data;
                setWorkflows(test);
        })
    }

    function handleAddWorkflow() {
        api.createWorkflowInstanceForB(selectedWF).then((d) => {
            getAllWorkflowInstances();
        });
        onHide();
    }

    return (
        <>
        <Form>
        {workflows.map((workflow) => (
            <div key={workflow.wfId} className="mb-3">
                <Form.Check 
                    type="radio"
                    id={workflow.wfId}
                    label={workflow.wfName}
                    checked={workflow.wfId === selectedWF.wfId}
                    onChange={() => setSelectedWF(workflow)}
                />
                <p>{workflow.wfDescription}</p>
            </div>
            ))
        }
        </Form>
        <Modal.Footer>
          <Button onClick={handleAddWorkflow}>{"Add"}</Button>
        </Modal.Footer>
        </>
    )
}

export default AddModal;