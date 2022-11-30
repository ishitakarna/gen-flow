import React from "react";
import { useState, useEffect } from "react";
import "./BusinessOwnerView.css"
import WorkflowTable from "./WorkflowTable/WorkflowTable";
import Button from 'react-bootstrap/Button';
import ModalView from '../ModalView/ModalView.js'
import ReportModal from "./ReportModal/ReportModal";
import SearchModal from "./SearchModal/SearchModal";

function BusinessOwnerView({bName}) {
    const [businessName, setBusinessName] = useState("");
    const [searchFilter, setSearchFilter] = useState("");
    const [addModalShow, setAddModalShow] = useState(false);
    const [reportModalShow, setReportModalShow] = useState(false);
    const [searchModalShow, setSearchModalShow] = useState(false);

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
                    <Button className = "bus-btn" variant="primary" onClick={() => setSearchModalShow(true)}>Search</Button>
                    <Button className = "bus-btn" variant="success" onClick={() => setAddModalShow(true)}>Add</Button>
                    <Button className = "bus-btn" variant="info" onClick={() => setReportModalShow(true)}>Report</Button>
                </div>
            </div>
            <div className = "bus-table">
                <WorkflowTable 
                addModalShow = {addModalShow}
                setAddModalShow = {setAddModalShow}/>
            </div>
            <ModalView
                show={reportModalShow}
                onHide={() => setReportModalShow(false)}
                modalheading = "Report"
                modaldata = {<ReportModal onHide={() => setReportModalShow(false)}/>}
            />
            <ModalView
                show={searchModalShow}
                modalheading = "Search"
                onHide={() => setSearchModalShow(false)}
                modaldata = {<SearchModal query={searchFilter} onHide={() => setSearchModalShow(false)}/>}
            />
        </div>
    )
}

export default BusinessOwnerView;