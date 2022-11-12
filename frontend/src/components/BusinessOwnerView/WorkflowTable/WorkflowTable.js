import React from "react";
import {useState, useEffect} from "react";
import {Table} from "react-bootstrap";
import Button from 'react-bootstrap/Button';
import "./WorkflowTable.css"
import Api from "../../../api";

function WorkflowTable() {
    const [workflowInstances, setWorkflowInstances] = useState([]);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
        getAllWorkflowInstances();
    }, []);

    function getAllWorkflowInstances() {
        const api = new Api();
        const wfData = []
        api.getIncompleteWorkFlowsForBO(1)
            .then(result => {
                let workflows = result.data
                Object.keys(workflows).forEach(function(key){
                    let wf = {}
                    let len = workflows[key].length
                    let val = workflows[key][len - 1]
                    console.log(val)
                    wf.wfInstanceId = val.wfInstanceId
                    wf.name = val.wfName
                    wf.dateC = val.wfcreatedDT
                    wf.dateU = val.wfupdatedDT
                    wf.curP = val.processId
                    wf.dept = val.deptId
                    wfData.push(wf)
                })
                // console.log(wfData)
            })
        const test = [
            {
                wfId: "red",
                name: "#f00",
                dateC: "12/10/22",
                curP: "do xyz",
                dateU: "14/10/22",
                dept: "abc"
            },
            {
                wfId: "green",
                name: "#0f0",
                dateC: "12/10/22",
                curP: "do xyz",
                dateU: "14/10/22",
                dept: "abc"
            },
            {
                wfId: "blue",
                name: "#00f",
                dateC: "12/10/22",
                curP: "do xyz",
                dateU: "14/10/22",
                dept: "abc"
            },
            {
                wfId: "cyan",
                name: "#0ff",
                dateC: "12/10/22",
                curP: "do xyz",
                dateU: "14/10/22",
                dept: "abc"
            },
            {
                wfId: "magenta",
                name: "#f0f",
                dateC: "12/10/22",
                curP: "do xyz",
                dateU: "14/10/22",
                dept: "abc"
            },
            {
                wfId: "yellow",
                name: "#ff0",
                dateC: "12/10/22",
                curP: "do xyz",
                dateU: "14/10/22",
                dept: "abc"
            },
            {
                wfId: "black",
                name: "#000",
                dateC: "12/10/22",
                curP: "do xyz",
                dateU: "14/10/22",
                dept: "abc"
            }
        ];
        setLoading(false);
        setWorkflowInstances(test);
    }

    if (isLoading) {
        return (
            <div className="wt-loader">
                <h1>Loading..</h1>
            </div>
        )
    }
    return (
        <div className="wt-container">
            <div className="wt-table_box">
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Workflow ID</th>
                        <th>Workflow Name</th>
                        <th>Date Created</th>
                        <th>Current Process</th>
                        <th>Last Updated</th>
                        <th>Cur. Process Dept.</th>
                    </tr>
                    </thead>
                    <tbody>
                    {workflowInstances.map(wfInst =>
                        <tr key={wfInst.wfId}>
                            <td>{wfInst.wfId}</td>
                            <td>{wfInst.name}</td>
                            <td>{wfInst.dateC}</td>
                            <td>{wfInst.curP}</td>
                            <td>{wfInst.dateU}</td>
                            <td>{wfInst.dept}</td>
                        </tr>
                    )}
                    </tbody>
                </Table>
            </div>
        </div>
    )
}

export default WorkflowTable;