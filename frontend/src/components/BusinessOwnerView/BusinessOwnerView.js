import React from "react";
import { useState, useEffect } from "react";
import "./BusinessOwnerView.css"
import WorkflowTable from "./WorkflowTable/WorkflowTable";
import Button from 'react-bootstrap/Button';
import ModalView from '../ModalView/ModalView.js'
import AddModal from "./AddModal/AddModal";
import ReportModal from "./ReportModal/ReportModal";

function BusinessOwnerView({bName}) {
    const [businessName, setBusinessName] = useState("");
    const [searchFilter, setSearchFilter] = useState("");
    const [addModalShow, setAddModalShow] = useState(false);
    const [reportModalShow, setReportModalShow] = useState(false);

    useEffect(() => {
        setBusinessName(bName);
    }, []);

    return (
        <div className="bus-container">
            <h1>
                {businessName}
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
                    <Button className = "bus-btn" variant="danger" onClick={() => setAddModalShow(true)}>Add</Button>
                    <Button className = "bus-btn" variant="primary" onClick={() => setReportModalShow(true)}>Report</Button>
                </div>
            </div>
            <div className = "bus-table">
                <WorkflowTable/>
            </div>
            <ModalView
                show={addModalShow}
                modalheading = "Workflows"
                onHide={() => setAddModalShow(false)}
                modaldata = {<AddModal onHide={() => setAddModalShow(false)}/>}
            />
            <ModalView
                show={reportModalShow}
                onHide={() => setReportModalShow(false)}
                modalheading = "Report"
                modaldata = {<ReportModal onHide={() => setReportModalShow(false)}/>}
            />
        </div>
    )
}

export default BusinessOwnerView;