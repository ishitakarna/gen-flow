import React from "react";
import { useState, useEffect } from "react";
import { Table } from "react-bootstrap";
import Button from 'react-bootstrap/Button';
import "./TableView.css"
import ModalView from '../../ModalView/ModalView.js'
import DetailModal from "./DetailModal/DetailModal";
import CompleteModal from "./CompleteModal/CompleteModal";
import Api from "../../../api";

function TableView({userId}) {
    const [workflowInstances, setWorkflowInstances] = useState([]);
    const [isLoading, setLoading] = useState(true);
    const [detailModalShow, setDetailModalShow] = useState(false);
    const [completeModalShow, setCompleteModalShow] = useState(false);
    const [clickedInstance, setClickedInstance] = useState({})
    const api = new Api();

    useEffect(() => {
        getAllWorkflowInstances();
    }, []);

    function getAllWorkflowInstances() {
        const wfData = []
        api.getWorkflowsForP(userId)
            .then(result => {
                let workflows = result.data;
                Object.keys(workflows).forEach(function(key){
                    let wf = {}
                    let val = workflows[key]
                    wf.dateC = val.wfcreatedDT
                    wf.curPId = val.processInstances[(val.processInstances).length - 1].processId
                    wf.processInstanceId = val.processInstances[(val.processInstances).length - 1].processInstanceId
                    wf.seqNumber = val.processInstances[(val.processInstances).length - 1].seqNumber
                    wf.wfId = val.wfId
                    wf.wfInstanceId = val.wfInstanceId
                    wfData.push(wf)
                })
                setWorkflowInstances(wfData);
                setLoading(false);
            })
    };

    if (isLoading) {
        return (
            <div className = "loader">
                <h1>Loading..</h1>
            </div>
        ) 
    }
    return (
        <div className="tv-container">
            <Table striped bordered hover>
            <thead>
                <tr>
                <th>Workflow Instance ID</th>
                <th>Date Created</th>
                <th>Details</th>
                <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {workflowInstances.map(wfInst =>
                        <tr className = "table_row" key={wfInst.wfInstanceId} onClick={() => setClickedInstance(wfInst)}>
                            <td>{wfInst.wfInstanceId}</td>
                            <td>{wfInst.dateC}</td>
                            <td className = "btn_row"><Button className = "tv-btn" variant="primary" onClick={() => setDetailModalShow(true)}>Details</Button>{' '}</td>
                            <td className = "btn_row"><Button className = "tv-btn" variant="outline-success" onClick={() => setCompleteModalShow(true)}>Complete</Button>{' '}</td>
                        </tr>
                )}
            </tbody>
            </Table>
            <ModalView
                show={detailModalShow}
                onHide={() => setDetailModalShow(false)}
                modalheading = "Workflow Instance Details"
                modaldata = {<DetailModal 
                    wfInst = {clickedInstance} 
                    onHide={() => setDetailModalShow(false)}/>}
            />
            <ModalView
                show={completeModalShow}
                onHide={() => setCompleteModalShow(false)}
                modalheading = "Set process completion parameters"
                modaldata = {<CompleteModal 
                    wfInst = {clickedInstance} 
                    userId = {userId}
                    setWorkflowInstances = {setWorkflowInstances}
                    onHide={() => setCompleteModalShow(false)}/>}
            />
        </div>
    )
}

export default TableView;