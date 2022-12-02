import React from "react";
import {useState, useEffect} from "react";
import {Table} from "react-bootstrap";
import "./WorkflowTable.css"
import Api from "../../../api";
import DeleteModal from "../DeleteModal/DeleteModal";
import AddModal from "../AddModal/AddModal";
import ModalView from '../../ModalView/ModalView.js'

function WorkflowTable({addModalShow, setAddModalShow}) {
    const [workflowInstances, setWorkflowInstances] = useState([]);
    const [isLoading, setLoading] = useState(true);
    const [deleteModalShow, setDeleteModalShow] = useState(false);
    const [selectedRow, setSelectedRow] = useState({});
    const deptMap = {
        1: "Kitchen",
        2: "Server",
        3: "Delivery Agent",
        4: "Janitor",
        5: "Cashier",
        6: "Manager"
    }

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
                    let val = workflows[key]
                    wf.wfInstanceId = val.wfInstanceId
                    wf.name = val.wfName
                    wf.dateC = val.wfcreatedDT
                    wf.dateU = val.wfupdatedDT
                    wf.curP = val.processInstances[(val.processInstances).length - 1].processName
                    wf.dept = deptMap[val.processInstances[(val.processInstances).length - 1].deptId]
                    wf.businessId = val.businessId
                    wfData.push(wf)
                })
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
            <ModalView
                show={addModalShow}
                modalheading = "Add Workflow"
                onHide={() => setAddModalShow(false)}
                modaldata = {<AddModal 
                    setLoading = {setLoading}
                    setWorkflowInstances = {setWorkflowInstances}
                    onHide={() => setAddModalShow(false)}/>}
            />
        </div>
    )
}

export default WorkflowTable;