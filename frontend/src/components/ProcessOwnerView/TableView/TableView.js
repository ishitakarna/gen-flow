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

    useEffect(() => {
        getAllWorkflowInstances();
    }, []);

    function getAllWorkflowInstances() {
        const api = new Api();
        const wfData = []
        api.getWorkflowsForP(2)
            .then(result => {
                let workflows = result.data;
                console.log(workflows)
                Object.keys(workflows).forEach(function(key){
                    let wf = {}
                    let len = workflows[key].length
                    let temp = workflows[key][len - 1]
                    let val = Object.values(temp)[0][0]
                    console.log(val)
                    // wf.wfInstanceId = val.wfInstanceId
                    // wf.name = val.wfName
                    // wf.dateC = val.wfcreatedDT
                    // wf.dateU = val.wfupdatedDT
                    // wf.curP = val.processId
                    // wf.dept = val.deptId
                    // wf.businessId = val.businessId
                    // wfData.push(wf)
                })
                // console.log(wfData);
                // setWorkflowInstances(wfData);
                // setLoading(false);
            })
       const test = [
        {
            wfId: "red",
            value: "#f00"
        },
        {
            wfId: "green",
            value: "#0f0"
        },
        {
            wfId: "blue",
            value: "#00f"
        },
        {
            wfId: "cyan",
            value: "#0ff"
        },
        {
            wfId: "magenta",
            value: "#f0f"
        },
        {
            wfId: "yellow",
            value: "#ff0"
        },
        {
            wfId: "black",
            value: "#000"
        }
        ];
        setLoading(false);
        setWorkflowInstances(test);
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
                <th>Date updated</th>
                <th>Details</th>
                <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {workflowInstances.map(wfInst =>
                        <tr className = "table_row" key={wfInst.wfId}>
                            <td>{wfInst.wfId}</td>
                            <td>{wfInst.value}</td>
                            <td className = "btn_row"><Button className = "tv-btn" variant="primary" onClick={() => setDetailModalShow(true)}>Details</Button>{' '}</td>
                            <td className = "btn_row"><Button className = "tv-btn" variant="outline-success" onClick={() => setCompleteModalShow(true)}>Complete</Button>{' '}</td>
                        </tr>
                )}
            </tbody>
            </Table>
            <ModalView
                show={detailModalShow}
                onHide={() => setDetailModalShow(false)}
                modalHeading = "Workflow Instance Details"
                modalData = {<DetailModal/>}
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