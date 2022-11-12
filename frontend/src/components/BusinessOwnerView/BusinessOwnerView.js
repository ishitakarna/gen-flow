import React from "react";
import { useState, useEffect } from "react";
import "./BusinessOwnerView.css"
import WorkflowTable from "./WorkflowTable/WorkflowTable";
import Button from 'react-bootstrap/Button';

function BusinessOwnerView() {
    const [businessName, setBusinessName] = useState("");
    const [searchFilter, setSearchFilter] = useState("");

    useEffect(() => {
        setBusinessName("X");
    }, []);

    return (
        <div className="bus-container">
            <h1>
                Business {businessName}
            </h1>
            <div className = "bus-filter">
                <div className = "bus-search-box">
                    <input id="filter"
                    name="filter"
                    type="text"
                    placeholder="Search a workflow instance"
                    value={searchFilter}
                    onChange = {e => setSearchFilter(e.target.value)}
                    />
                </div>
                <div>
                    <Button className = "bus-btn" variant="danger">Add</Button>
                    <Button className = "bus-btn" variant="primary">Report</Button>
                </div>
            </div>
            <div className = "bus-table">
                <WorkflowTable/>
            </div>
        </div>
    )
}

export default BusinessOwnerView;