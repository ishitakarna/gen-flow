import React from "react";
import {useState, useEffect} from "react";
import {Table} from "react-bootstrap";
import Button from 'react-bootstrap/Button';
import "./WorkflowTable.css"
import Api from "../../../api";
import DeleteModal from "../DeleteModal/DeleteModal";
import ModalView from '../../ModalView/ModalView.js'

function WorkflowTable() {
    const [workflowInstances, setWorkflowInstances] = useState([]);
    const [isLoading, setLoading] = useState(true);
    const [deleteModalShow, setDeleteModalShow] = useState(false);
    const [selectedRow, setSelectedRow] = useState({});

    useEffect(() => {
        getAllWorkflowInstances();
    }, []);

    function getAllWorkflowInstances() {
        const api = new Api();
        const wfData = []
        api.getIncompleteWorkFlowsForBO(1)
            .then(result => {
                let workflows = result.data;
                Object.keys(workflows).forEach(function(key){
                    let wf = {}
                    let len = workflows[key].length
                    let temp = workflows[key][len - 1]
                    let val = Object.values(temp)[0][0]
                    wf.wfInstanceId = val.wfInstanceId
                    wf.name = val.wfName
                    wf.dateC = val.wfcreatedDT
                    wf.dateU = val.wfupdatedDT
                    wf.curP = val.processName
                    wf.dept = val.deptId
                    wf.businessId = val.businessId
                    wfData.push(wf)
                })
                console.log(wfData);
                setWorkflowInstances(wfData);
                setLoading(false);
            })
    }

    function handleRowClick(wfInst) {
        setSelectedRow(wfInst);
        setDeleteModalShow(true);
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
                        <th>Workflow Inst. ID</th>
                        <th>Workflow Name</th>
                        <th>Date Created</th>
                        <th>Current Process</th>
                        <th>Last Updated</th>
                        <th>Cur. Process Dept.</th>
                    </tr>
                    </thead>
                    <tbody>
                    {workflowInstances.map(wfInst =>
                        <tr key={wfInst.wfInstanceId} onClick={() => handleRowClick(wfInst)}>
                            <td>{wfInst.wfInstanceId}</td>
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
            <ModalView
                show={deleteModalShow}
                onHide={() => setDeleteModalShow(false)}
                modalheading = "Delete Workflow Instance"
                modaldata = {<DeleteModal
                    setLoading = {setLoading}
                    setWorkflowInstances = {setWorkflowInstances}
                    deleteData = {selectedRow}
                    onHide={() => {setDeleteModalShow(false);}}/>}
            />
        </div>
    )
}

export default WorkflowTable;