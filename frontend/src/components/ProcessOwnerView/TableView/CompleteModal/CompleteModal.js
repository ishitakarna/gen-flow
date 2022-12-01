import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Api from "../../../../api";
import { useState, useEffect } from "react";
import { Form } from 'react-bootstrap';

function CompleteModal({wfInst, onHide}) {
    const api = new Api();
    const [processParams, setProcessParams] = useState([]);
    const [isLoading, setLoading] = useState(true);
    const [paramValues, setParamValues] = useState({});

    useEffect(() => {
        getProcessCompletionParams();
    }, []);

    function handleComplete() {
        let data = {}
        data.processInstanceId = wfInst.processInstanceId
        data.seqNumber = wfInst.seqNumber
        data.wfId = wfInst.wfId
        data.wfInstanceId = wfInst.wfInstanceId
        data.params = []

        Object.keys(processParams).forEach(function(key){
            let param = {}
            let val = processParams[key]
            param.paramId = val.paramId
            param.processInstanceId = wfInst.processInstanceId
            param.paramVal = paramValues[val.paramName]
            data.params.push(param)
        })

        api.completedProcess(data).then((d) => {
            console.log(d.data)
            //getAllWorkflowInstances();
        })
        onHide()
    }

    function handleInputChange(param, e) {
        setParamValues(prevParams => ({...prevParams, [param.paramName]: e.target.value}))
    }

    function getProcessCompletionParams() {
        let paramList = []
        let paramStore = {}
        api.getProcessParams(wfInst.curPId)
            .then(result => {
                let params = result.data
                Object.keys(params).forEach(function(key){
                    let p = {}
                    let val = params[key]
                    p.paramId = val.paramId
                    p.paramName = val.paramName
                    p.paramType = val.paramType
                    paramList.push(p)
                    paramStore[val.paramName] = ""
                })
                setProcessParams(paramList)
                setLoading(false)
                setParamValues(paramStore)
            })
    }

    if (isLoading) {
        return (
            <div className="wt-loader">
                <h1>Loading..</h1>
            </div>
        )
    }
    return (
        <>
        <Form>
        {processParams.map((param) => (
            <div key={param.paramId} className="mb-3">
                <Form.Group className="mb-3">
                    <Form.Label>{param.paramName}</Form.Label>
                    <Form.Control 
                    value={paramValues[param.paramName] || ''}
                    type={param.paramType} 
                    placeholder={`Enter ${param.paramName}`}
                    onChange={(e) => handleInputChange(param, e)}
                    />
                </Form.Group>
            </div>
            ))
        }
        </Form>
        <Modal.Footer>
          <Button onClick={handleComplete}>{"Complete"}</Button>
        </Modal.Footer>
        </>
    )
}
export default CompleteModal;