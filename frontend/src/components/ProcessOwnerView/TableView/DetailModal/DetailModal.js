import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Api from "../../../../api";
import { useState, useEffect } from "react";

function DetailModal({wfInst, onHide}) {
    const api = new Api();
    const [workflowDetails, setWorkflowDetails] = useState({});

    useEffect(() => {
        getWorkflowDetails();
    }, []);

    function getWorkflowDetails() {
        let test = [];
        let wfData = [];

        api.getWorkflowDetails(wfInst.wfInstanceId)
            .then(result => {
                let processes = result.data;
                console.log(test);
                Object.keys(processes).forEach(function(key){
                    let wf = {}
                    let len = processes[key].length
                    let temp = processes[key][len - 1]
                    console.log(temp)
                    let val = Object.values(temp)[0][0]
                    //console.log(val)
                    wf.wfInstanceId = val.wfInstanceId
                    wf.name = val.wfName
                    wf.dateC = val.wfcreatedDT
                    wf.dateU = val.wfupdatedDT
                    wf.curP = val.processId
                    wf.dept = val.deptId
                    wf.businessId = val.businessId
                    wfData.push(wf)
                })
                //setWorkflowDetails(test);
        })
    }

    return (
        <>
        <Modal.Footer>
          <Button onClick={onHide}>{"Close"}</Button>
        </Modal.Footer>
        </>
    )
}

export default DetailModal;