import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Api from "../../../api";
import {useEffect, useState} from "react";

function SearchModal(props) {

    const [workflow, setWorkflow] = useState([]);

    useEffect(() => {
        getWfData();
    }, []);

    function getWfData() {
        const api = new Api()
        api.searchWorkflowInstanceId(props.query)
            .then(result => {
                let workflows = result.data;
                Object.keys(workflows).forEach(function(key){
                    let len = workflows[key].length
                    let temp = workflows[key][len - 1]
                    setWorkflow(JSON.stringify(temp))
                })
            })
    }
    return (
        <>
            {workflow}
        <Modal.Footer>
        </Modal.Footer>
        </>
    )
}

export default SearchModal;