import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useState, useEffect } from "react";
import Api from "../../../api";
import { ListGroup } from 'react-bootstrap';

function ReportModal(props) {
    const [report, setReport] = useState([]);
    const [imageReport, setImageReport] = useState("");
    const api = new Api();

    useEffect(() => {
        getReport();
    }, []);

    function getReport() {
        let wfData = [];

        api.getReport(1)
            .then(result => {
                let test = result.data.completed_counts;
                let image = result.data.trend_image;
                test.forEach(function(item, index) {
                    let wf = {}
                    wf.completedWFInstances = item.completedWFInstances;
                    wf.wfName = item.wfName;
                    wfData.push(wf)
                })
                console.log(image)
                setReport(wfData)
                setImageReport(image)
        })
    }

    return (
        <>
        {report.map((wf) => (
            <ListGroup key={wf.wfName} className="mb-3">
                <ListGroup.Item><b>Workflow: </b> {wf.wfName}</ListGroup.Item>
                <ListGroup.Item><b>Completed Workflow Instances: </b> {wf.completedWFInstances}</ListGroup.Item>
                <br/>
            </ListGroup>
            ))
        }
        <img height={200} width={200} src={"data:image/png;base64," +  imageReport} />
        <Modal.Footer>
          <Button onClick = {props.onHide} >{"Close"}</Button>
        </Modal.Footer>
        </>
    )
}

export default ReportModal;