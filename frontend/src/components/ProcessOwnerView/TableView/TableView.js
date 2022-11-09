import React from "react";
import { useState, useEffect } from "react";
import { Table } from "react-bootstrap";
import Button from 'react-bootstrap/Button';
import "./TableView.css"

function TableView() {
    const [workflowInstances, setWorkflowInstances] = useState([]);
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
        getAllWorkflowInstances();
    }, []);

    function getAllWorkflowInstances() {
       const test = [
        {
            wfId: "red",
            value: "#f00"
        },
        {
            wfId: "green",
            value: "#0f0"
        },
        {
            wfId: "blue",
            value: "#00f"
        },
        {
            wfId: "cyan",
            value: "#0ff"
        },
        {
            wfId: "magenta",
            value: "#f0f"
        },
        {
            wfId: "yellow",
            value: "#ff0"
        },
        {
            wfId: "black",
            value: "#000"
        }
        ];
        setLoading(false);
        setWorkflowInstances(test);
    };

    if (isLoading) {
        return (
            <div className = "loader">
                <h1>Loading..</h1>
            </div>
        ) 
    }
    return (
        <div className="container">
            <div className = "table_box">
            <Table striped bordered hover>
            <thead>
                <tr>
                <th>Workflow ID</th>
                <th>Date updated</th>
                <th>Details</th>
                <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {workflowInstances.map(wfInst =>
                        <tr className = "table_row" key={wfInst.wfId}>
                            <td>{wfInst.wfId}</td>
                            <td>{wfInst.value}</td>
                            <td className = "btn_row"><Button className = "btn" variant="primary">Details</Button>{' '}</td>
                            <td className = "btn_row"><Button className = "btn" variant="outline-success">Complete</Button>{' '}</td>
                        </tr>
                )}
            </tbody>
            </Table>
            </div>
        </div>
    )
}

export default TableView;