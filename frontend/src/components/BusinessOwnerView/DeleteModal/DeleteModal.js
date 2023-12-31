import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Api from "../../../api";

function DeleteModal({setLoading, setWorkflowInstances, deleteData, onHide}) {
    const api = new Api();
    const deptMap = {
        1: "Kitchen",
        2: "Server",
        3: "Delivery Agent",
        4: "Janitor",
        5: "Cashier",
        6: "Manager"
    }

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

    function handleDeleteWorkflowInst() {
        api.deleteWorkflowInstance(deleteData).then((d) => {
            getAllWorkflowInstances();
        });
        onHide();
    }

    return (
        <>
        <h5>All data associated with this workflow instance will be deleted.</h5>
        <h6>Are you sure you want to delete <b style={{color: "red"}}>Workflow Instance {deleteData.wfInstanceId}?</b></h6>
        <Modal.Footer>
          <Button onClick={handleDeleteWorkflowInst}>{"Delete"}</Button>
        </Modal.Footer>
        </>
    )
}

export default DeleteModal;