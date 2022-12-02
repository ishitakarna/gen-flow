import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Api from "../../../../api";
import { useState, useEffect } from "react";
import { ListGroup } from 'react-bootstrap';

function DetailModal({wfInst, onHide}) {
    const api = new Api();
    const [workflowDetails, setWorkflowDetails] = useState([]);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
        getWorkflowDetails();
    }, []);

    function getWorkflowDetails() {
        api.getWorkflowDetails(wfInst.wfInstanceId)
            .then(result => {
                let processes = result.data;
                Object.keys(processes).forEach(function(key){
                    let wf = {}
                    let val = processes[key]
                    wf.businessId = val.businessId
                    wf.wfDescription = val.wfDescription
                    wf.wfInstanceId = val.wfInstanceId
                    wf.wfName = val.wfName
                    wf.createdDT = val.createdDT
                    wf.updatedDT = val.updatedDT
                    wf.completedDT = val.completedDT
                    wf.processes = val.processInstances
                    console.log(val)
                    setWorkflowDetails(wf)
                    setLoading(false)
                })
        })
    }

    if (isLoading) {
        return (
            <div className="wt-loader">
                <h1>Loading..</h1>
                <Modal.Footer>
                </Modal.Footer>
            </div>
        )
    }
    return (
        <>
        <ListGroup>
            <ListGroup.Item><b>Workflow Instance: </b>{workflowDetails.wfInstanceId}</ListGroup.Item>
            <ListGroup.Item><b>Name: </b>{workflowDetails.wfName}</ListGroup.Item>
            <ListGroup.Item><b>Description: </b>{workflowDetails.wfDescription}</ListGroup.Item>
            <ListGroup.Item>
                <b>Processes: </b>
                {workflowDetails.processes.map((processInst, i , row) => (
                    <ul key={processInst.processName} className="mb-3">
                        {i == workflowDetails.processes.length - 1? 
                            <li style={{color: "red"}}>
                                {processInst.processName}
                            </li> :
                            <li style={{color: "green"}}>
                                {processInst.processName}
                                {processInst.paramInstances.map((param) => (
                                    <ul>
                                        <li>{param.paramName}: <b>{param.paramVal}</b></li>
                                    </ul>
                                ))}
                            </li>
                        }
                    </ul>
            ))}
            </ListGroup.Item>
        </ListGroup>
        <Modal.Footer>
          <Button onClick={onHide}>{"Close"}</Button>
        </Modal.Footer>
        </>
    )
}

export default DetailModal;