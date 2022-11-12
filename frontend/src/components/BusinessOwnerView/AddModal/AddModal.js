import Form from 'react-bootstrap/Form';
import { useState, useEffect } from "react";

function AddModal() {
    const [workflows, setWorkflows] = useState([]);
    const [selectedWF, setSelectedWF] = useState(1);

    useEffect(() => {
        getAllWorkflows();
    }, []);

    function getAllWorkflows() {
        const test = [
            {
                wfId : 1,
                wfName: "Online Food Order"
            },
            {
                wfId : 2,
                wfName: "Dine In Order"
            }
        ];
        setWorkflows(test);
    };

    return (
        <>
        <Form>
        {workflows.map((workflow) => (
            <div key={workflow.wfId} className="mb-3">
                <Form.Check 
                    type="radio"
                    id={workflow.wfId}
                    label={workflow.wfName}
                    checked={workflow.wfId == selectedWF}
                    onChange={() => setSelectedWF(workflow.wfId)}
                />
            </div>
            ))
        }
        </Form>
        </>
    )
}

export default AddModal;