import React from "react";
import { useState, useEffect } from "react";
import TableView from "./TableView/TableView";
import "./ProcessOwnerView.css"

function ProcessOwnerView({businessName}) {
    const [processName, setProcessName] = useState("");
    const [searchFilter, setSearchFilter] = useState("");

    useEffect(() => {
        setProcessName(businessName)
    }, []);

    return (
        <div className="container">
            <h1>
                Process in {processName}
            </h1>
            {/* <div className = "search-box">
                <input id="filter"
                name="filter"
                type="text"
                placeholder="Search Workflow Instance"
                value={searchFilter}
                onChange = {e => setSearchFilter(e.target.value)}
                />
            </div> */}
            <div className="table-view">
                <TableView/>
            </div>
        </div>
    )
}

export default ProcessOwnerView;