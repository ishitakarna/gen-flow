import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Api from "../../../api";

function DeleteModal({setLoading, setWorkflowInstances, deleteData, onHide}) {
    const api = new Api();

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
                    wf.curP = val.processId
                    wf.dept = val.deptId
                    wf.businessId = val.businessId
                    wfData.push(wf)
                })
                console.log(wfData);
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
        <h6>Are you sure you want to delete?</h6>
        <Modal.Footer>
          <Button onClick={handleDeleteWorkflowInst}>{"Delete"}</Button>
        </Modal.Footer>
        </>
    )
}

export default DeleteModal;