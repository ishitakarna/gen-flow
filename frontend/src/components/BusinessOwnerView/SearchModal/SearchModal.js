import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Api from "../../../api";
import {useEffect, useState} from "react";
import { ListGroup } from 'react-bootstrap';

function SearchModal(props) {

    const [workflow, setWorkflow] = useState([]);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
        getWfData();
    }, []);

    async function getWfData() {
        const api = new Api()
        await api.searchWorkflowInstanceId(props.query)
            .then(result => {
                let workflows = result.data;
                Object.keys(workflows).forEach(function(key){
                    let wf = {}
                    let val = workflows[key]
                    console.log(val)
                    wf.businessId = val.businessId
                    wf.wfDescription = val.wfDescription
                    wf.wfInstanceId = val.wfInstanceId
                    wf.wfName = val.wfName
                    wf.createdDT = val.createdDT
                    wf.updatedDT = val.updatedDT
                    wf.completedDT = val.completedDT
                    wf.processes = val.processInstances
                    setWorkflow(wf)
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
            <ListGroup.Item><b>Workflow Instance: </b>{workflow.wfInstanceId}</ListGroup.Item>
            <ListGroup.Item><b>Name: </b>{workflow.wfName}</ListGroup.Item>
            <ListGroup.Item><b>Description: </b>{workflow.wfDescription}</ListGroup.Item>
            <ListGroup.Item>
                <b>Processes: </b>
                {workflow.processes.map((processInst, i , row) => (
                    <ul key={processInst.processName} className="mb-3">
                        {i == workflow.processes.length - 1? 
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
        </Modal.Footer>
        </>
    )
}

export default SearchModal;