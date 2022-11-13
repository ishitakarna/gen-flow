import Form from 'react-bootstrap/Form';
import { useState, useEffect } from "react";
import Api from "../../../api";
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function AddModal(props) {
    const [workflows, setWorkflows] = useState([]);
    const [selectedWF, setSelectedWF] = useState({});
    const api = new Api();

    useEffect(() => {
        getAllWorkflows();
    }, []);

    function getAllWorkflows() {
        let test = [];

        api.getWorkflowsForB(1)
            .then(result => {
                test = result.data;
                setWorkflows(test);
        })
    }

    function handleAddWorkflow() {
        api.createWorkflowInstanceForB(selectedWF).then((d) => {
            console.log(d.data);
        });
        props.onHide();
    }

    return (
        <>
        <Form>
        {workflows.map((workflow) => (
            <div key={workflow.wfId} className="mb-3">
                <Form.Check 
                    type="radio"
                    id={workflow.wfId}
                    label={workflow.wfName}
                    checked={workflow.wfId === selectedWF.wfId}
                    onChange={() => setSelectedWF(workflow)}
                />
                <p>{workflow.wfDescription}</p>
            </div>
            ))
        }
        </Form>
        <Modal.Footer>
          <Button onClick={handleAddWorkflow}>{"Add"}</Button>
        </Modal.Footer>
        </>
    )
}

export default AddModal;