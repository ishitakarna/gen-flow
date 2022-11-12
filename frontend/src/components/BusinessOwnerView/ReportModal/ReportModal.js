import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useState, useEffect } from "react";
import Api from "../../../api";

function ReportModal(props) {
    const [report, setReport] = useState([]);
    const api = new Api();

    useEffect(() => {
        getReport();
    }, []);

    function getReport() {
        let wfData = [];

        api.getReport(1)
            .then(result => {
                let test = result.data;
                test.forEach(function(item, index) {
                    let wf = {}
                    wf.completedWFInstances = item.completedWFInstances;
                    wf.wfName = item.wfName;
                    wfData.push(wf)
                })
                console.log(wfData)
                setReport(wfData);
        })
    }

    return (
        <>
        {report.map((wf) => (
            <ul key={wf.wfName} className="mb-3">
                <li>Workflow: {wf.wfName}</li>
                <li>Completed Workflow Instances: {wf.completedWFInstances}</li>
            </ul>
            ))
        }
        <Modal.Footer>
          <Button onClick = {props.onHide} >{"Close"}</Button>
        </Modal.Footer>
        </>
    )
}

export default ReportModal;