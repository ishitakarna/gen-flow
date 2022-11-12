import React from "react";
import { useState, useEffect } from "react";
import { Table } from "react-bootstrap";
import Button from 'react-bootstrap/Button';
import "./TableView.css"
import ModalView from '../../ModalView/ModalView.js'
import DetailModal from "./DetailModal/DetailModal";
import CompleteModal from "./CompleteModal/CompleteModal";
import Api from "../../../api";

function TableView() {
    const [workflowInstances, setWorkflowInstances] = useState([]);
    const [isLoading, setLoading] = useState(true);
    const [detailModalShow, setDetailModalShow] = useState(false);
    const [completeModalShow, setCompleteModalShow] = useState(false);
    const [clickedInstance, setClickedInstance] = useState({})

    useEffect(() => {
        getAllWorkflowInstances();
    }, []);

    function getAllWorkflowInstances() {
        const api = new Api();
        const wfData = []
        api.getWorkflowsForP(2)
            .then(result => {
                let workflows = result.data;
                Object.keys(workflows).forEach(function(key){
                    let wf = {}
                    let len = workflows[key].length
                    let temp = workflows[key][len - 1]
                    let val = Object.values(temp)[0][0]
                    wf.wfInstanceId = val.wfInstanceId
                    wf.dateC = val.createdDT
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
                modaldata = {<DetailModal wfInst = {clickedInstance} onHide={() => setDetailModalShow(false)}/>}
            />
            <ModalView
                show={completeModalShow}
                onHide={() => setCompleteModalShow(false)}
                modalHeading = "Process completion parameters"
                modalData = {<CompleteModal/>}
            />
        </div>
    )
}

export default TableView;