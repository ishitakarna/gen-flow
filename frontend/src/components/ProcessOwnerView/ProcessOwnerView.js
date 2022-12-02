import React from "react";
import { useState, useEffect } from "react";
import TableView from "./TableView/TableView";
import "./ProcessOwnerView.css"

function ProcessOwnerView({businessName, userId, userName}) {
    const [processName, setProcessName] = useState("");
    const deptMap = {
        1: "Kitchen",
        2: "Server",
        3: "Delivery Agent",
        4: "Janitor",
        5: "Cashier",
        6: "Manager"
    }

    useEffect(() => {
        setProcessName(businessName)
    }, []);

    return (
        <div className="container">
            <h1>{processName}</h1>
            <h2 style={{color:"green"}}>
                Department: {deptMap[userId]}
            </h2>
            <h3>Hi! <span style={{color:"blue", textTransform:"capitalize"}}>{userName}</span></h3>
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
                <TableView userId = {userId}/>
            </div>
        </div>
    )
}

export default ProcessOwnerView;